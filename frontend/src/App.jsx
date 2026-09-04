import React, { useEffect, useState } from 'react';
import { fetchRecentTransactions, connectWebSocket } from './services/api';
import { AlertTriangle, ShieldAlert, ShieldCheck, Activity, CreditCard } from 'lucide-react';
import { LineChart, Line, XAxis, YAxis, Tooltip, ResponsiveContainer } from 'recharts';

export default function App() {
  const [transactions, setTransactions] = useState([]);
  const [stats, setStats] = useState({ total: 0, highRisk: 0, totalAmount: 0 });

  useEffect(() => {
    // Initial Load from DB
    fetchRecentTransactions().then((data) => {
      setTransactions(data);
      updateStats(data);
    });

    // Real-Time Streaming Listener
    const ws = connectWebSocket((newTxn) => {
      setTransactions((prev) => {
        const updated = [newTxn, ...prev.slice(0, 49)];
        updateStats(updated);
        return updated;
      });
    });

    return () => ws.close();
  }, []);

  const updateStats = (txns) => {
    const total = txns.length;
    const highRisk = txns.filter((t) => t.risk_level === 'HIGH').length;
    const totalAmount = txns.reduce((sum, t) => sum + (t.amount || 0), 0);
    setStats({ total, highRisk, totalAmount: totalAmount.toFixed(2) });
  };

  return (
    <div style={{ backgroundColor: '#0f172a', color: '#f8fafc', minHeight: '100vh', padding: '24px', fontFamily: 'sans-serif' }}>
      {/* Header */}
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '24px', borderBottom: '1px solid #334155', paddingBottom: '16px' }}>
        <div>
          <h1 style={{ fontSize: '24px', fontWeight: 'bold', margin: 0, display: 'flex', alignItems: 'center', gap: '10px' }}>
            <ShieldAlert color="#ef4444" size={28} /> AI Real-Time Fraud & Risk Analytics Platform
          </h1>
          <p style={{ color: '#94a3b8', margin: '4px 0 0 0', fontSize: '14px' }}>Automated ML Inference & Anomaly Monitoring Dashboard</p>
        </div>
        <div style={{ display: 'flex', alignItems: 'center', gap: '8px', backgroundColor: '#1e293b', padding: '8px 16px', borderRadius: '20px', border: '1px solid #10b981' }}>
          <Activity color="#10b981" size={18} />
          <span style={{ fontSize: '13px', color: '#10b981', fontWeight: '600' }}>LIVE STREAM ACTIVE</span>
        </div>
      </div>

      {/* Analytics Metric Cards */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: '16px', marginBottom: '24px' }}>
        <div style={{ backgroundColor: '#1e293b', padding: '20px', borderRadius: '12px', border: '1px solid #334155' }}>
          <div style={{ color: '#94a3b8', fontSize: '14px' }}>Total Processed Transactions</div>
          <div style={{ fontSize: '28px', fontWeight: 'bold', marginTop: '8px' }}>{stats.total}</div>
        </div>
        <div style={{ backgroundColor: '#1e293b', padding: '20px', borderRadius: '12px', border: '1px solid #ef4444' }}>
          <div style={{ color: '#ef4444', fontSize: '14px', fontWeight: '600' }}>Flagged High Risk Anomalies</div>
          <div style={{ fontSize: '28px', fontWeight: 'bold', marginTop: '8px', color: '#ef4444' }}>{stats.highRisk}</div>
        </div>
        <div style={{ backgroundColor: '#1e293b', padding: '20px', borderRadius: '12px', border: '1px solid #334155' }}>
          <div style={{ color: '#94a3b8', fontSize: '14px' }}>Total Stream Value</div>
          <div style={{ fontSize: '28px', fontWeight: 'bold', marginTop: '8px', color: '#38bdf8' }}>${stats.totalAmount}</div>
        </div>
      </div>

      {/* Live Chart Visualizer */}
      <div style={{ backgroundColor: '#1e293b', padding: '20px', borderRadius: '12px', marginBottom: '24px', border: '1px solid #334155' }}>
        <h3 style={{ margin: '0 0 16px 0', fontSize: '16px', color: '#cbd5e1' }}>Real-Time Risk Score Volatility Stream</h3>
        <ResponsiveContainer width="100%" height={180}>
          <LineChart data={[...transactions].reverse()}>
            <XAxis dataKey="transaction_id" stroke="#64748b" />
            <YAxis domain={[0, 1]} stroke="#64748b" />
            <Tooltip contentStyle={{ backgroundColor: '#0f172a', borderColor: '#334155' }} />
            <Line type="monotone" dataKey="risk_score" stroke="#ef4444" strokeWidth={2} dot={false} />
          </LineChart>
        </ResponsiveContainer>
      </div>

      {/* Live Transactions Feed Table */}
      <div style={{ backgroundColor: '#1e293b', borderRadius: '12px', border: '1px solid #334155', overflow: 'hidden' }}>
        <div style={{ padding: '16px 20px', borderBottom: '1px solid #334155', fontWeight: 'bold' }}>Live Transaction Logs</div>
        <table style={{ width: '100%', borderCollapse: 'collapse', textAlign: 'left', fontSize: '14px' }}>
          <thead>
            <tr style={{ backgroundColor: '#0f172a', color: '#94a3b8' }}>
              <th style={{ padding: '12px 20px' }}>Txn ID</th>
              <th>Customer</th>
              <th>Amount</th>
              <th>Merchant</th>
              <th>Location</th>
              <th>Risk Score</th>
              <th>Status</th>
            </tr>
          </thead>
          <tbody>
            {transactions.map((txn, index) => (
              <tr key={index} style={{ borderBottom: '1px solid #334155' }}>
                <td style={{ padding: '12px 20px', fontWeight: '600' }}>{txn.transaction_id}</td>
                <td>{txn.customer_id}</td>
                <td>${txn.amount}</td>
                <td>{txn.merchant}</td>
                <td>{txn.location}</td>
                <td>
                  <span style={{
                    fontWeight: 'bold',
                    color: txn.risk_score >= 0.75 ? '#ef4444' : txn.risk_score >= 0.4 ? '#f59e0b' : '#10b981'
                  }}>
                    {(txn.risk_score * 100).toFixed(1)}%
                  </span>
                </td>
                <td>
                  {txn.risk_level === 'HIGH' ? (
                    <span style={{ backgroundColor: '#450a0a', color: '#ef4444', padding: '4px 8px', borderRadius: '4px', fontSize: '12px', fontWeight: 'bold' }}>HIGH RISK</span>
                  ) : txn.risk_level === 'MEDIUM' ? (
                    <span style={{ backgroundColor: '#451a03', color: '#f59e0b', padding: '4px 8px', borderRadius: '4px', fontSize: '12px', fontWeight: 'bold' }}>MEDIUM RISK</span>
                  ) : (
                    <span style={{ backgroundColor: '#064e3b', color: '#10b981', padding: '4px 8px', borderRadius: '4px', fontSize: '12px', fontWeight: 'bold' }}>CLEARED</span>
                  )}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}