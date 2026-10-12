from pathlib import Path

DATA = {
 '01_kickoff.md': '''# Acme Health — Project Kickoff (September 9)
Owner: Maya Chen, Customer Success. Target production launch: October 30.
Business goal: reduce patient support wait time by 35% and automate 40% of routine inquiries without exposing protected health information (PHI).
Success metrics: p95 response latency under 3 seconds, answer accuracy at least 95% on approved evaluation set, zero critical privacy incidents, and escalation to a human for uncertain medical questions.
Stakeholders: Elena Ruiz (VP Operations, sponsor), Ravi Patel (Engineering Lead), Dr. Kim (Clinical Safety), Maya Chen (CSM).
''',
 '02_architecture.md': '''# Architecture Review (October 3)
Acme's assistant uses a web chat frontend, API gateway, retrieval service, vector index of approved FAQs, LLM answer generation, and ticketing integration.
Production authentication uses SSO. Audit logging is implemented in staging but production retention settings are not verified. Encryption in transit is enabled.
Open architecture item: PHI redaction must run before logs and external model requests. Ravi owns the redaction gate. No evidence of production sign-off yet.
''',
 '03_support_ticket.md': '''# Support Ticket ACME-184 (October 7)
Severity: High. Status: Open. Owner: Ravi Patel.
In staging, the assistant occasionally includes a patient name in the diagnostic trace sent to the observability provider. Reproduced in 2 of 50 tests.
Mitigation proposed: pre-logging PHI scrubber and regression suite. Fix is not yet deployed or validated. This is a launch blocker until verified by security.
''',
 '04_eval_report.md': '''# Evaluation Report (October 8)
Owner: Dr. Kim. Dataset: 200 approved patient-support questions.
Correct answers: 182/200 (91%). Target is at least 95%.
Medical uncertainty escalation: 18/20 correct (90%). Target is 100% for the critical escalation scenarios.
Failure themes: insurance eligibility edge cases, unsupported treatment advice, and outdated appointment instructions.
Recommended: add curated FAQs, improve refusal/escalation instructions, rerun held-out evaluation.
''',
 '05_performance.md': '''# Load Test (October 9)
Owner: Ravi Patel. 100 concurrent users, 30-minute staging test.
p95 latency: 4.2 seconds, versus target under 3 seconds. Error rate: 0.8%, versus target under 1%.
Vector search contributes 1.4 seconds at p95. Suggested optimizations: caching, index tuning, and reducing retrieval payload. No production-equivalent retest yet.
''',
 '06_customer_meeting.md': '''# Customer Weekly Meeting (October 10)
Elena Ruiz reiterated that the October 30 launch date is important for a board demonstration. She requested a go/no-go recommendation by October 23.
Maya Chen explained that security validation, clinical evaluation, and latency remain open. Elena asked for daily blocker updates and a contingency plan for a limited internal pilot if the full launch slips.
Action: Ravi to deliver PHI remediation evidence by October 16; Dr. Kim to rerun evaluation by October 19; Maya to prepare decision memo by October 23.
''',
 '07_security_policy.md': '''# Acme Health AI Launch Policy
Any confirmed PHI leakage to third-party systems blocks external production launch until remediation and independent verification.
Clinical escalation must pass all critical test cases. Approved evaluation accuracy must be at least 95%. Security lead must approve logging controls and data retention.
A restricted internal pilot with synthetic data may be approved separately; it is not equivalent to production approval.
''',
 '08_action_tracker.md': '''# Launch Action Tracker (October 11)
OPEN — ACME-184 PHI trace leakage; Ravi; due October 16; security verification required.
OPEN — Accuracy 91% versus 95% threshold; Dr. Kim; due October 19.
OPEN — Critical escalation 90% versus 100% threshold; Dr. Kim; due October 19.
OPEN — p95 latency 4.2s versus 3s target; Ravi; due October 20.
OPEN — Production audit log retention sign-off; Security Lead; due October 21.
PLANNED — Go/no-go review; Maya and Elena; October 23.
''',
 '09_older_status.md': '''# Older Status Update (September 24)
Project status: Green. Initial prototype achieved 97% accuracy on a 30-question development set. Team expects October 30 launch.
NOTE: This is an older small development test, not the later 200-question approved evaluation.
''',
}

def generate(directory=Path(__file__).parent / 'data'):
    directory = Path(directory)
    directory.mkdir(parents=True, exist_ok=True)
    for name, content in DATA.items():
        (directory / name).write_text(content, encoding='utf-8')
    return len(DATA)

if __name__ == '__main__':
    print(f'Generated {generate()} synthetic documents')
