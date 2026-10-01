"""
Vireo Audio SLA Analyst - Verification & Validation Suite
=========================================================
Runs automated sanity and accuracy checks against supplied CSV data
and compares against baseline metrics in the execution guide.
"""

import sys
from sla_engine import SLAEngine

def run_validation():
    print("==========================================================")
    print("      VIREO AUDIO SUPPORT SLA ANALYST - VALIDATION")
    print("==========================================================")
    
    engine = SLAEngine()
    engine.load_data()
    engine.process_tickets()
    engine.map_historical_roster()
    kpis = engine.get_summary_kpis()
    
    passed = 0
    total_tests = 0
    
    def check(test_name: str, actual, expected, tolerance=1e-3):
        nonlocal passed, total_tests
        total_tests += 1
        if isinstance(expected, (int, float)):
            diff = abs(actual - expected)
            is_pass = diff <= tolerance
        else:
            is_pass = (actual == expected)
            
        status = "PASSED [PASS]" if is_pass else f"FAILED [FAIL] (Expected {expected}, Got {actual})"
        print(f"[{total_tests:02d}] {test_name:<45} : {status}")
        if is_pass:
            passed += 1

    # Validation Checks matching Section 11 of Execution Guide
    check("Raw Ticket Row Count", kpis['raw_ticket_rows'], 11816)
    check("Unique Ticket ID Count", kpis['unique_tickets'], 11200)
    check("Duplicate Rows Removed", kpis['duplicate_rows_removed'], 616)
    check("Total Unique SLA Breaches", kpis['total_breaches'], 2440)
    check("Overall Breach Rate (%)", kpis['overall_breach_rate'], 21.7857, tolerance=1e-2)
    check("SLA Credit Exposure (INR)", kpis['sla_credit_exposure_inr'], 854000)
    check("Tier 1 Ticket Count", kpis['t1_tickets'], 10448)
    check("Tier 1 SLA Breaches", kpis['t1_breaches'], 2265)
    check("Tier 1 Breach Rate (%)", kpis['t1_breach_rate'], 21.6788, tolerance=1e-2)
    check("Tier 1 Morning Shift Tickets", kpis['t1_morning_tickets'], 5803)
    check("Tier 1 Morning Shift Breaches", kpis['t1_morning_breaches'], 1866)
    check("Tier 1 Morning Breach Rate (%)", kpis['t1_morning_breach_rate'], 32.1558, tolerance=1e-2)
    check("Morning Breaches Created Overnight", kpis['morning_overnight_breaches'], 1452)
    check("Morning Overnight Breach Share (%)", kpis['morning_overnight_breach_share'], 77.8135, tolerance=1e-2)
    check("Normal Hour Morning Breach Rate (%)", kpis['morning_normal_breach_rate'], 11.0224, tolerance=1e-2)
    check("Overnight Morning Breach Rate (%)", kpis['morning_overnight_breach_rate'], 70.9331, tolerance=1e-2)

    print("----------------------------------------------------------")
    if total_tests > 0:
        pct_passed = (passed / total_tests) * 100
    else:
        pct_passed = 0.0
    print(f"RESULTS: {passed}/{total_tests} Tests Passed ({pct_passed:.1f}%)")
    print("==========================================================")
    
    if passed == total_tests:
        print("ALL VERIFICATION CHECKS PASSED SUCCESSFULLY!")
        return 0
    else:
        print("SOME CHECKS FAILED. PLEASE INSPECT LOGS.")
        return 1

if __name__ == '__main__':
    sys.exit(run_validation())
