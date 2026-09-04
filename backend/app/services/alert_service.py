import logging
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("AlertEngine")

class AlertService:
    def __init__(self):
        self.risk_threshold = 0.75

    def process_transaction_alert(self, txn_data: dict):
        """Evaluates risk score and dispatches notifications for high-risk anomalies."""
        risk_score = txn_data.get("risk_score", 0.0)
        transaction_id = txn_data.get("transaction_id")
        amount = txn_data.get("amount")
        customer_id = txn_data.get("customer_id")

        if risk_score >= self.risk_threshold:
            self.send_email_alert(transaction_id, customer_id, amount, risk_score)
            self.send_slack_webhook(transaction_id, customer_id, amount, risk_score)

    def send_email_alert(self, txn_id: str, cust_id: str, amount: float, score: float):
        subject = f"🚨 HIGH RISK FRAUD ALERT: Transaction {txn_id}"
        body = (
            f"ALERT TRIGGERED AT {datetime.utcnow()} UTC\n"
            f"----------------------------------------\n"
            f"Transaction ID : {txn_id}\n"
            f"Customer ID    : {cust_id}\n"
            f"Amount         : ${amount:.2f}\n"
            f"Calculated Risk: {score * 100:.1f}%\n"
            f"Action Required: Freeze account and initiate manual audit.\n"
        )
        logger.warning(f"\n[EMAIL DISPATCHED] -> To: security-team@bank.com\nSubject: {subject}\n{body}")

    def send_slack_webhook(self, txn_id: str, cust_id: str, amount: float, score: float):
        logger.warning(
            f"[ALERT CHANNEL] ⚠️ High Risk Transaction Flagged! "
            f"ID: {txn_id} | Customer: {cust_id} | Amount: ${amount:.2f} | Score: {score:.2f}"
        )

alert_engine = AlertService()