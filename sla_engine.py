"""
Vireo Audio Support SLA Analytical Engine
==========================================
Deterministic analytical engine for calculating first-response SLA breaches,
financial credit exposure, roster time-matching, shift breakdowns, and overnight ticket signals.
"""

import os
import glob
from typing import Dict, Tuple, Optional
import pandas as pd
import numpy as np

# SLA targets by channel in minutes
SLA_TARGETS_MINUTES = {
    'chat': 15,
    'voice': 120,
    'social': 240,
    'email': 480
}

SLA_CREDIT_PER_BREACH_INR = 350

class SLAEngine:
    def __init__(self, data_dir: str = "."):
        self.data_dir = data_dir
        self.tickets_raw: Optional[pd.DataFrame] = None
        self.agents_raw: Optional[pd.DataFrame] = None
        self.orders_raw: Optional[pd.DataFrame] = None
        self.customers_raw: Optional[pd.DataFrame] = None
        self.products_raw: Optional[pd.DataFrame] = None
        
        self.tickets_clean: Optional[pd.DataFrame] = None
        self.tickets_rostered: Optional[pd.DataFrame] = None
        
    def find_file(self, pattern: str) -> str:
        """Find a file matching a pattern in data_dir or Data subdirectory."""
        matches = glob.glob(os.path.join(self.data_dir, pattern))
        if not matches:
            matches = glob.glob(os.path.join(self.data_dir, "Data", pattern))
        if not matches:
            # Try searching without directory prefix if pattern already contains path
            matches = glob.glob(pattern)
        if not matches:
            raise FileNotFoundError(f"Could not find any file matching pattern: {pattern}")
        return matches[0]

    def load_data(self) -> None:
        """Load raw CSV datasets."""
        tickets_path = self.find_file("*tickets.csv")
        agents_path = self.find_file("*agents.csv")
        
        self.tickets_raw = pd.read_csv(tickets_path)
        self.agents_raw = pd.read_csv(agents_path)
        
        # Optional datasets
        try:
            self.orders_raw = pd.read_csv(self.find_file("*orders.csv"))
        except FileNotFoundError:
            self.orders_raw = pd.DataFrame()
            
        try:
            self.customers_raw = pd.read_csv(self.find_file("*customers.csv"))
        except FileNotFoundError:
            self.customers_raw = pd.DataFrame()
            
        try:
            self.products_raw = pd.read_csv(self.find_file("*products.csv"))
        except FileNotFoundError:
            self.products_raw = pd.DataFrame()

    def process_tickets(self) -> pd.DataFrame:
        """
        Clean ticket data:
        1. Deduplicate by ticket_id (keep first canonical row).
        2. Parse UTC timestamps and convert to IST (Asia/Kolkata).
        3. Calculate first response duration in minutes.
        4. Evaluate SLA target and breach flag.
        5. Calculate SLA credit exposure (₹350).
        6. Treat CSAT = 0 as legacy missing response.
        7. Tag creation hour, shift, and week.
        """
        if self.tickets_raw is None:
            self.load_data()
            
        # 1. Deduplicate
        df = self.tickets_raw.drop_duplicates(subset=['ticket_id'], keep='first').copy()
        
        # 2. Parse timestamps as UTC and convert to IST
        df['created_at_dt_utc'] = pd.to_datetime(df['created_at'], utc=True)
        df['first_response_at_dt_utc'] = pd.to_datetime(df['first_response_at'], utc=True)
        df['resolved_at_dt_utc'] = pd.to_datetime(df['resolved_at'], utc=True, errors='coerce')
        
        df['created_at_ist'] = df['created_at_dt_utc'].dt.tz_convert('Asia/Kolkata')
        df['first_response_at_ist'] = df['first_response_at_dt_utc'].dt.tz_convert('Asia/Kolkata')
        
        # 3. First response duration in minutes
        df['response_minutes'] = (
            df['first_response_at_dt_utc'] - df['created_at_dt_utc']
        ).dt.total_seconds() / 60.0
        
        # 4. Channel SLA target and Breach flag
        df['channel_clean'] = df['channel'].str.lower().str.strip()
        df['sla_target_minutes'] = df['channel_clean'].map(SLA_TARGETS_MINUTES)
        
        # Breach = first response LATER than target (exact target is not a breach)
        df['is_breach'] = df['response_minutes'] > df['sla_target_minutes']
        
        # 5. Financial impact
        df['sla_credit_inr'] = df['is_breach'].astype(int) * SLA_CREDIT_PER_BREACH_INR
        
        # 6. Legacy CSAT handling (0 means no response in legacy Freshdesk export)
        df['csat_valid'] = df['csat_score'].apply(lambda x: np.nan if pd.isna(x) or x == 0 else float(x))
        
        # 7. Date / Time breakdown in IST
        df['created_date_ist'] = df['created_at_ist'].dt.date
        df['created_hour_ist'] = df['created_at_ist'].dt.hour
        df['created_week_ist'] = df['created_at_ist'].dt.tz_localize(None).dt.to_period('W-MON').dt.start_time.dt.date
        
        # Tag shift of ticket creation in IST:
        # Morning: 06:00 to 13:59 (6 <= hour < 14)
        # Day: 14:00 to 21:59 (14 <= hour < 22)
        # Night: 22:00 to 05:59 (hour >= 22 or hour < 6)
        def get_shift_from_hour(hour: int) -> str:
            if 6 <= hour < 14:
                return 'Morning'
            elif 14 <= hour < 22:
                return 'Day'
            else:
                return 'Night'
                
        df['creation_shift_ist'] = df['created_hour_ist'].apply(get_shift_from_hour)
        df['is_created_overnight'] = df['created_hour_ist'].apply(lambda h: True if (h >= 22 or h < 6) else False)
        
        self.tickets_clean = df
        return df

    def map_historical_roster(self) -> pd.DataFrame:
        """
        Time-match tickets to historical agent roster in agents.csv using ticket created_at timestamp.
        Assumptions: Ticket agent_id represents resolving agent. We time-match agent roster assignment
        where created_at_ist falls in [from_date, to_date].
        """
        if self.tickets_clean is None:
            self.process_tickets()
            
        agents_df = self.agents_raw.copy()
        
        # Parse roster dates in IST
        agents_df['from_dt_ist'] = pd.to_datetime(agents_df['from_date']).dt.tz_localize('Asia/Kolkata')
        # Fill missing to_date with far-future date (active assignment) and make end of day inclusive
        agents_df['to_dt_ist'] = pd.to_datetime(
            agents_df['to_date'].fillna('2099-12-31')
        ).dt.tz_localize('Asia/Kolkata') + pd.Timedelta(days=1) - pd.Timedelta(1, unit='ns')
        
        # Merge on agent_id
        merged = pd.merge(
            self.tickets_clean,
            agents_df[['agent_id', 'name', 'site', 'team', 'shift', 'tier', 'from_dt_ist', 'to_dt_ist']],
            on='agent_id',
            how='left',
            suffixes=('', '_roster')
        )
        
        # Filter rows matching time window
        valid_mask = (
            (merged['created_at_ist'] >= merged['from_dt_ist']) &
            (merged['created_at_ist'] <= merged['to_dt_ist'])
        )
        
        # Fallback for tickets unmatched by timestamp (keep first match if any)
        rostered_df = merged[valid_mask].copy()
        
        # Check if any ticket lost in mapping
        unmatched_ids = set(self.tickets_clean['ticket_id']) - set(rostered_df['ticket_id'])
        if unmatched_ids:
            # Handle unmatched fallback by taking closest agent info
            unmatched_df = merged[merged['ticket_id'].isin(unmatched_ids)].drop_duplicates(subset=['ticket_id'])
            rostered_df = pd.concat([rostered_df, unmatched_df], ignore_index=True)
            
        self.tickets_rostered = rostered_df
        return rostered_df

    def get_summary_kpis(self) -> Dict:
        """Calculate high-level project KPIs."""
        if self.tickets_rostered is None:
            self.map_historical_roster()
            
        raw_rows = len(self.tickets_raw)
        unique_tickets = len(self.tickets_clean)
        duplicates_removed = raw_rows - unique_tickets
        
        total_breaches = int(self.tickets_clean['is_breach'].sum())
        breach_rate = float(self.tickets_clean['is_breach'].mean() * 100)
        total_credit_exposure = total_breaches * SLA_CREDIT_PER_BREACH_INR
        
        t1_df = self.tickets_rostered[self.tickets_rostered['tier'] == 1]
        t2_df = self.tickets_rostered[self.tickets_rostered['tier'] == 2]
        
        t1_count = len(t1_df)
        t1_breaches = int(t1_df['is_breach'].sum())
        t1_breach_rate = float(t1_df['is_breach'].mean() * 100) if t1_count > 0 else 0.0
        
        t1_m = t1_df[t1_df['shift'] == 'Morning']
        t1_m_count = len(t1_m)
        t1_m_breaches = int(t1_m['is_breach'].sum())
        t1_m_breach_rate = float(t1_m['is_breach'].mean() * 100) if t1_m_count > 0 else 0.0
        
        m_overnight = t1_m[t1_m['is_created_overnight']]
        m_normal = t1_m[~t1_m['is_created_overnight']]
        
        m_overnight_breaches = int(m_overnight['is_breach'].sum())
        m_overnight_breach_share = (m_overnight_breaches / t1_m_breaches * 100) if t1_m_breaches > 0 else 0.0
        
        m_normal_breach_rate = float(m_normal['is_breach'].mean() * 100) if len(m_normal) > 0 else 0.0
        m_overnight_breach_rate = float(m_overnight['is_breach'].mean() * 100) if len(m_overnight) > 0 else 0.0
        
        return {
            'raw_ticket_rows': raw_rows,
            'unique_tickets': unique_tickets,
            'duplicate_rows_removed': duplicates_removed,
            'total_breaches': total_breaches,
            'overall_breach_rate': breach_rate,
            'sla_credit_exposure_inr': total_credit_exposure,
            't1_tickets': t1_count,
            't1_breaches': t1_breaches,
            't1_breach_rate': t1_breach_rate,
            't2_tickets': len(t2_df),
            't2_breaches': int(t2_df['is_breach'].sum()),
            't1_morning_tickets': t1_m_count,
            't1_morning_breaches': t1_m_breaches,
            't1_morning_breach_rate': t1_m_breach_rate,
            'morning_overnight_breaches': m_overnight_breaches,
            'morning_overnight_breach_share': m_overnight_breach_share,
            'morning_normal_breach_rate': m_normal_breach_rate,
            'morning_overnight_breach_rate': m_overnight_breach_rate
        }

    def get_weekly_trends(self) -> pd.DataFrame:
        """Get weekly aggregated breach rates and credit exposure."""
        if self.tickets_rostered is None:
            self.map_historical_roster()
            
        t1 = self.tickets_rostered[self.tickets_rostered['tier'] == 1]
        
        weekly = t1.groupby('created_week_ist').agg(
            total_tickets=('ticket_id', 'count'),
            breaches=('is_breach', 'sum'),
            breach_rate=('is_breach', lambda x: x.mean() * 100),
            sla_credit_inr=('sla_credit_inr', 'sum')
        ).reset_index()
        
        weekly['created_week_ist'] = pd.to_datetime(weekly['created_week_ist']).dt.strftime('%Y-%m-%d')
        return weekly

    def get_shift_breakdown(self) -> pd.DataFrame:
        """Get metrics grouped by rostered shift for Tier 1 agents."""
        if self.tickets_rostered is None:
            self.map_historical_roster()
            
        t1 = self.tickets_rostered[self.tickets_rostered['tier'] == 1]
        
        shift_df = t1.groupby('shift').agg(
            tickets=('ticket_id', 'count'),
            breaches=('is_breach', 'sum'),
            breach_rate=('is_breach', lambda x: x.mean() * 100),
            sla_credit_inr=('sla_credit_inr', 'sum'),
            avg_response_min=('response_minutes', 'mean')
        ).reset_index()
        
        return shift_df.sort_values(by='breach_rate', ascending=False)

    def get_agent_leaderboard(self) -> pd.DataFrame:
        """Get agent-level performance table."""
        if self.tickets_rostered is None:
            self.map_historical_roster()
            
        agent_df = self.tickets_rostered.groupby(['agent_id', 'name', 'shift', 'tier', 'site']).agg(
            tickets=('ticket_id', 'count'),
            breaches=('is_breach', 'sum'),
            breach_rate=('is_breach', lambda x: x.mean() * 100),
            sla_credit_inr=('sla_credit_inr', 'sum'),
            avg_csat=('csat_valid', 'mean'),
            avg_response_min=('response_minutes', 'mean')
        ).reset_index()
        
        return agent_df.sort_values(by='breaches', ascending=False)

    def get_channel_breakdown(self) -> pd.DataFrame:
        """Get metrics by channel."""
        if self.tickets_clean is None:
            self.process_tickets()
            
        ch_df = self.tickets_clean.groupby('channel').agg(
            tickets=('ticket_id', 'count'),
            breaches=('is_breach', 'sum'),
            breach_rate=('is_breach', lambda x: x.mean() * 100),
            sla_credit_inr=('sla_credit_inr', 'sum'),
            avg_response_min=('response_minutes', 'mean'),
            sla_target_min=('sla_target_minutes', 'first')
        ).reset_index()
        
        return ch_df.sort_values(by='breaches', ascending=False)

    def get_june_reshuffle_analysis(self) -> pd.DataFrame:
        """Analyze breach pattern before and after June 30, 2025 roster change."""
        if self.tickets_rostered is None:
            self.map_historical_roster()
            
        t1 = self.tickets_rostered[self.tickets_rostered['tier'] == 1].copy()
        t1['period'] = np.where(
            t1['created_at_ist'] < pd.Timestamp('2025-06-30', tz='Asia/Kolkata'),
            'Pre-June Reshuffle (Jan-Jun 2025)',
            'Post-June Reshuffle (Jul 2025+)'
        )
        
        reshuffle_summary = t1.groupby(['period', 'shift']).agg(
            tickets=('ticket_id', 'count'),
            breaches=('is_breach', 'sum'),
            breach_rate=('is_breach', lambda x: x.mean() * 100),
            overnight_created_share=('is_created_overnight', lambda x: x.mean() * 100)
        ).reset_index()
        
        return reshuffle_summary


if __name__ == '__main__':
    engine = SLAEngine()
    engine.load_data()
    engine.process_tickets()
    engine.map_historical_roster()
    kpis = engine.get_summary_kpis()
    print("=== SLA ENGINE VERIFIED KPIS ===")
    for k, v in kpis.items():
        print(f"{k}: {v}")
