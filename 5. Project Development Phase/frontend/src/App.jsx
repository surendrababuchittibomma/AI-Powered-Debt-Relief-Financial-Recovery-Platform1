import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { 
  LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, BarChart, Bar, Cell, PieChart, Pie
} from 'recharts';
import { 
  User as UserIcon, Shield, CreditCard, Activity, FileText, Plus, Trash2, LogOut, CheckCircle, AlertTriangle, Cpu, TrendingUp
} from 'lucide-react';

const API_BASE = 'http://localhost:8000/api';

export default function App() {
  const [token, setToken] = useState(localStorage.getItem('token') || '');
  const [user, setUser] = useState(null);
  const [activeTab, setActiveTab] = useState('dashboard');
  const [authMode, setAuthMode] = useState('login'); // 'login' or 'register'
  
  // Auth Form State
  const [authForm, setAuthForm] = useState({ name: '', email: '', password: '' });
  const [authError, setAuthError] = useState('');

  // Financial Profile State
  const [profile, setProfile] = useState({ monthly_income: '4500.00', monthly_expenses: '2200.00', existing_debts: '500.00', financial_health_score: 0 });
  const [profileForm, setProfileForm] = useState({ monthly_income: '', monthly_expenses: '', existing_debts: '' });
  const [profileMsg, setProfileMsg] = useState('');

  // Loans State
  const [loans, setLoans] = useState([]);
  const [loanForm, setLoanForm] = useState({ loan_type: 'Credit Card', loan_amount: '', outstanding_amount: '', interest_rate: '', due_date: '' });
  const [loanError, setLoanError] = useState('');

  // AI & Settlement States
  const [settlements, setSettlements] = useState([]);
  const [selectedLoan, setSelectedLoan] = useState(null);
  const [negotiationResult, setNegotiationResult] = useState(null);
  const [isEvaluating, setIsEvaluating] = useState(false);
  const [isNegotiating, setIsNegotiating] = useState(false);

  // Setup Axios defaults
  useEffect(() => {
    if (token) {
      axios.defaults.headers.common['Authorization'] = `Bearer ${token}`;
      localStorage.setItem('token', token);
      fetchUserData();
    } else {
      delete axios.defaults.headers.common['Authorization'];
      localStorage.removeItem('token');
      setUser(null);
    }
  }, [token]);

  const fetchUserData = async () => {
    try {
      // Get profile
      const profRes = await axios.get(`${API_BASE}/profile`);
      setProfile(profRes.data);
      setProfileForm({
        monthly_income: profRes.data.monthly_income,
        monthly_expenses: profRes.data.monthly_expenses,
        existing_debts: profRes.data.existing_debts
      });
    } catch (err) {
      console.log("No profile found yet");
    }
    fetchLoans();
    fetchSettlements();
  };

  const fetchLoans = async () => {
    try {
      const res = await axios.get(`${API_BASE}/loans`);
      setLoans(res.data);
    } catch (err) {
      console.error(err);
    }
  };

  const fetchSettlements = async () => {
    try {
      const res = await axios.get(`${API_BASE}/settlements`);
      setSettlements(res.data);
    } catch (err) {
      console.error(err);
    }
  };

  const handleAuthSubmit = async (e) => {
    e.preventDefault();
    setAuthError('');
    try {
      if (authMode === 'login') {
        const res = await axios.post(`${API_BASE}/auth/login`, {
          email: authForm.email,
          password: authForm.password
        });
        setToken(res.data.access_token);
        setUser({ email: authForm.email });
      } else {
        await axios.post(`${API_BASE}/auth/register`, authForm);
        setAuthMode('login');
        setAuthError('Registration successful! Please login.');
      }
    } catch (err) {
      setAuthError(err.response?.data?.detail || 'Authentication operation failed.');
    }
  };

  const handleSaveProfile = async (e) => {
    e.preventDefault();
    setProfileMsg('');
    try {
      const res = await axios.post(`${API_BASE}/profile`, profileForm);
      setProfile(res.data);
      setProfileMsg('Financial profile updated successfully!');
      fetchSettlements(); // Recalculate settlement contexts
    } catch (err) {
      setProfileMsg(err.response?.data?.detail || 'Failed to update profile.');
    }
  };

  const handleAddLoan = async (e) => {
    e.preventDefault();
    setLoanError('');
    try {
      await axios.post(`${API_BASE}/loans`, loanForm);
      setLoanForm({ loan_type: 'Credit Card', loan_amount: '', outstanding_amount: '', interest_rate: '', due_date: '' });
      fetchLoans();
    } catch (err) {
      setLoanError(err.response?.data?.detail || 'Failed to add loan record.');
    }
  };

  const handleDeleteLoan = async (loanId) => {
    try {
      await axios.delete(`${API_BASE}/loans/${loanId}`);
      fetchLoans();
      fetchSettlements();
    } catch (err) {
      console.error(err);
    }
  };

  const handleEvaluateSettlement = async (loan) => {
    setSelectedLoan(loan);
    setIsEvaluating(true);
    setNegotiationResult(null);
    try {
      await axios.post(`${API_BASE}/settlements/evaluate/${loan.loan_id}`);
      await fetchSettlements();
      setActiveTab('negotiation');
    } catch (err) {
      alert(err.response?.data?.detail || 'Evaluation failed. Make sure you set a financial profile first.');
    } finally {
      setIsEvaluating(false);
    }
  };

  const handleGenerateNegotiation = async (loanId) => {
    setIsNegotiating(true);
    try {
      const res = await axios.post(`${API_BASE}/negotiate/${loanId}`);
      setNegotiationResult(res.data);
    } catch (err) {
      alert(err.response?.data?.detail || 'Failed to compile AI negotiation.');
    } finally {
      setIsNegotiating(false);
    }
  };

  const handleLogout = () => {
    setToken('');
  };

  // Auth View
  if (!token) {
    return (
      <div className="animate-fade-in" style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', minHeight: '100vh', padding: '20px' }}>
        <div className="glass-card" style={{ width: '100%', maxLength: '450px', maxWidth: '450px' }}>
          <div style={{ textAlign: 'center', marginBottom: '32px' }}>
            <div style={{ display: 'inline-flex', padding: '12px', background: 'var(--color-primary-glow)', borderRadius: '12px', marginBottom: '16px' }}>
              <Cpu size={32} color="var(--color-primary)" />
            </div>
            <h1 className="text-gradient" style={{ fontSize: '2rem', fontWeight: 700 }}>FinRelief AI</h1>
            <p style={{ color: 'var(--color-text-muted)', fontSize: '0.9rem', marginTop: '8px' }}>
              AI-Powered Debt Relief & Financial Recovery
            </p>
          </div>

          <form onSubmit={handleAuthSubmit} style={{ display: 'flex', flexDirection: 'column', gap: '20px' }}>
            {authMode === 'register' && (
              <div>
                <label>Full Name</label>
                <input 
                  type="text" 
                  placeholder="John Doe" 
                  required 
                  value={authForm.name}
                  onChange={e => setAuthForm({...authForm, name: e.target.value})}
                />
              </div>
            )}
            <div>
              <label>Email Address</label>
              <input 
                type="email" 
                placeholder="john@example.com" 
                required 
                value={authForm.email}
                onChange={e => setAuthForm({...authForm, email: e.target.value})}
              />
            </div>
            <div>
              <label>Password</label>
              <input 
                type="password" 
                placeholder="••••••••" 
                required 
                value={authForm.password}
                onChange={e => setAuthForm({...authForm, password: e.target.value})}
              />
            </div>

            {authError && (
              <div style={{ background: 'rgba(244, 63, 94, 0.1)', color: 'var(--color-danger)', border: '1px solid rgba(244, 63, 94, 0.2)', padding: '10px', borderRadius: '6px', fontSize: '0.85rem', display: 'flex', alignItems: 'center', gap: '8px' }}>
                <AlertTriangle size={16} />
                <span>{authError}</span>
              </div>
            )}

            <button className="bg-gradient-btn" type="submit" style={{ width: '100%' }}>
              {authMode === 'login' ? 'Sign In' : 'Create Account'}
            </button>
          </form>

          <div style={{ textAlign: 'center', marginTop: '24px', fontSize: '0.9rem' }}>
            <span style={{ color: 'var(--color-text-muted)' }}>
              {authMode === 'login' ? "Don't have an account? " : "Already have an account? "}
            </span>
            <span 
              style={{ color: 'var(--color-primary)', cursor: 'pointer', fontWeight: 600 }}
              onClick={() => {
                setAuthMode(authMode === 'login' ? 'register' : 'login');
                setAuthError('');
              }}
            >
              {authMode === 'login' ? 'Register' : 'Login'}
            </span>
          </div>
        </div>
      </div>
    );
  }

  // Dashboard Stats Calculations
  const totalOutstanding = loans.reduce((acc, curr) => acc + parseFloat(curr.outstanding_amount), 0);
  const incomeVal = parseFloat(profile.monthly_income) || 0;
  const expenseVal = parseFloat(profile.monthly_expenses) || 0;
  const monthlySavings = incomeVal - expenseVal;

  const barChartData = [
    { name: 'Income', amount: incomeVal, fill: 'var(--color-primary)' },
    { name: 'Expenses', amount: expenseVal, fill: 'var(--color-warning)' },
    { name: 'Total Debt', amount: totalOutstanding, fill: 'var(--color-danger)' },
  ];

  const debtDistributionData = loans.map(l => ({
    name: l.loan_type,
    value: parseFloat(l.outstanding_amount)
  }));

  const COLORS = ['#6366f1', '#06b6d4', '#f59e0b', '#f43f5e', '#10b981'];

  return (
    <div className="dashboard-layout">
      {/* Sidebar Navigation */}
      <aside className="sidebar">
        <div>
          <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
            <div style={{ padding: '8px', background: 'var(--color-primary-glow)', borderRadius: '8px' }}>
              <Cpu size={24} color="var(--color-primary)" />
            </div>
            <h2 className="text-gradient" style={{ fontSize: '1.4rem', fontWeight: 700 }}>FinRelief AI</h2>
          </div>

          <div className="nav-links">
            <div className={`nav-item ${activeTab === 'dashboard' ? 'active' : ''}`} onClick={() => setActiveTab('dashboard')}>
              <Activity size={20} />
              <span>Dashboard</span>
            </div>
            <div className={`nav-item ${activeTab === 'profile' ? 'active' : ''}`} onClick={() => setActiveTab('profile')}>
              <UserIcon size={20} />
              <span>Financial Profile</span>
            </div>
            <div className={`nav-item ${activeTab === 'loans' ? 'active' : ''}`} onClick={() => setActiveTab('loans')}>
              <CreditCard size={20} />
              <span>My Loans</span>
            </div>
            <div className={`nav-item ${activeTab === 'negotiation' ? 'active' : ''}`} onClick={() => setActiveTab('negotiation')}>
              <FileText size={20} />
              <span>AI Settlement</span>
            </div>
          </div>
        </div>

        <button className="btn-secondary" onClick={handleLogout} style={{ width: '100%', gap: '12px' }}>
          <LogOut size={18} />
          <span>Sign Out</span>
        </button>
      </aside>

      {/* Main Content Body */}
      <main style={{ padding: '40px', overflowY: 'auto', height: '100vh' }}>
        
        {/* TAB 1: DASHBOARD */}
        {activeTab === 'dashboard' && (
          <div className="animate-fade-in" style={{ display: 'flex', flexDirection: 'column', gap: '32px' }}>
            <div>
              <h1 style={{ fontSize: '2.2rem', fontWeight: 700 }}>Overview</h1>
              <p style={{ color: 'var(--color-text-muted)', marginTop: '4px' }}>Real-time settlement probabilities and financial metrics.</p>
            </div>

            {/* Metric Blocks */}
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(240px, 1fr))', gap: '24px' }}>
              <div className="glass-card" style={{ display: 'flex', flexDirection: 'column', gap: '8px' }}>
                <span style={{ color: 'var(--color-text-muted)', fontSize: '0.85rem', fontWeight: 600 }}>MONTHLY DISPOSABLE INCOME</span>
                <span style={{ fontSize: '2rem', fontWeight: 700, color: 'var(--color-primary)' }}>${incomeVal.toLocaleString(undefined, { minimumFractionDigits: 2 })}</span>
              </div>
              <div className="glass-card" style={{ display: 'flex', flexDirection: 'column', gap: '8px' }}>
                <span style={{ color: 'var(--color-text-muted)', fontSize: '0.85rem', fontWeight: 600 }}>MONTHLY SAVINGS</span>
                <span style={{ fontSize: '2rem', fontWeight: 700, color: monthlySavings >= 0 ? 'var(--color-success)' : 'var(--color-danger)' }}>
                  ${monthlySavings.toLocaleString(undefined, { minimumFractionDigits: 2 })}
                </span>
              </div>
              <div className="glass-card" style={{ display: 'flex', flexDirection: 'column', gap: '8px' }}>
                <span style={{ color: 'var(--color-text-muted)', fontSize: '0.85rem', fontWeight: 600 }}>TOTAL OUTSTANDING DEBT</span>
                <span style={{ fontSize: '2rem', fontWeight: 700, color: 'var(--color-danger)' }}>${totalOutstanding.toLocaleString(undefined, { minimumFractionDigits: 2 })}</span>
              </div>
              <div className="glass-card" style={{ display: 'flex', flexDirection: 'column', gap: '8px' }}>
                <span style={{ color: 'var(--color-text-muted)', fontSize: '0.85rem', fontWeight: 600 }}>FINANCIAL HEALTH SCORE</span>
                <div style={{ display: 'flex', alignItems: 'center', gap: '12px', marginTop: '4px' }}>
                  <span style={{ fontSize: '2rem', fontWeight: 700, color: 'var(--color-secondary)' }}>{profile.financial_health_score || 0}</span>
                  <span style={{ fontSize: '0.85rem', color: 'var(--color-text-muted)' }}>/ 100</span>
                </div>
              </div>
            </div>

            {/* Visual Charts */}
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(400px, 1fr))', gap: '24px' }}>
              <div className="glass-card">
                <h3 style={{ marginBottom: '20px', fontSize: '1.1rem' }}>Financial Summary</h3>
                <div style={{ height: '300px' }}>
                  <ResponsiveContainer width="100%" height="100%">
                    <BarChart data={barChartData}>
                      <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.05)" />
                      <XAxis dataKey="name" stroke="var(--color-text-muted)" />
                      <YAxis stroke="var(--color-text-muted)" />
                      <Tooltip contentStyle={{ background: 'var(--bg-main)', border: '1px solid var(--border-color)' }} />
                      <Bar dataKey="amount">
                        {barChartData.map((entry, index) => (
                          <Cell key={`cell-${index}`} fill={entry.fill} />
                        ))}
                      </Bar>
                    </BarChart>
                  </ResponsiveContainer>
                </div>
              </div>

              <div className="glass-card">
                <h3 style={{ marginBottom: '20px', fontSize: '1.1rem' }}>Debt Distribution</h3>
                <div style={{ height: '300px', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
                  {debtDistributionData.length > 0 ? (
                    <ResponsiveContainer width="100%" height="100%">
                      <PieChart>
                        <Pie
                          data={debtDistributionData}
                          cx="50%"
                          cy="50%"
                          innerRadius={60}
                          outerRadius={100}
                          paddingAngle={5}
                          dataKey="value"
                        >
                          {debtDistributionData.map((entry, index) => (
                            <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                          ))}
                        </Pie>
                        <Tooltip contentStyle={{ background: 'var(--bg-main)', border: '1px solid var(--border-color)' }} />
                      </PieChart>
                    </ResponsiveContainer>
                  ) : (
                    <span style={{ color: 'var(--color-text-muted)' }}>No debts recorded. Please add loans.</span>
                  )}
                </div>
              </div>
            </div>

            {/* Quick action evaluated list */}
            <div className="glass-card">
              <h3 style={{ marginBottom: '16px' }}>Settlement Possibilities Summary</h3>
              {settlements.length > 0 ? (
                <div style={{ overflowX: 'auto' }}>
                  <table>
                    <thead>
                      <tr>
                        <th>Loan ID</th>
                        <th>Settlement Probability</th>
                        <th>Recommended Payoff</th>
                        <th>Priority</th>
                        <th>Evaluation Date</th>
                      </tr>
                    </thead>
                    <tbody>
                      {settlements.map((s, idx) => (
                        <tr key={idx}>
                          <td>#{s.loan_id}</td>
                          <td>
                            <span className={`badge ${s.settlement_prediction.includes('High') ? 'badge-success' : s.settlement_prediction.includes('Medium') ? 'badge-warning' : 'badge-danger'}`}>
                              {s.settlement_prediction}
                            </span>
                          </td>
                          <td style={{ fontWeight: 600 }}>${parseFloat(s.recommended_amount).toLocaleString(undefined, { minimumFractionDigits: 2 })}</td>
                          <td>
                            <span className={`badge ${s.priority_level === 'Critical' ? 'badge-danger' : s.priority_level === 'High' ? 'badge-warning' : 'badge-success'}`}>
                              {s.priority_level}
                            </span>
                          </td>
                          <td style={{ color: 'var(--color-text-muted)' }}>{new Date(s.created_at).toLocaleDateString()}</td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              ) : (
                <p style={{ color: 'var(--color-text-muted)' }}>No evaluations performed yet. Go to **My Loans** to initiate an AI analysis.</p>
              )}
            </div>
          </div>
        )}

        {/* TAB 2: FINANCIAL PROFILE */}
        {activeTab === 'profile' && (
          <div className="animate-fade-in" style={{ display: 'flex', flexDirection: 'column', gap: '32px', maxWidth: '650px' }}>
            <div>
              <h1 style={{ fontSize: '2.2rem', fontWeight: 700 }}>Financial Capacity Profile</h1>
              <p style={{ color: 'var(--color-text-muted)', marginTop: '4px' }}>Provide income and expense parameters to run settlement risk modeling.</p>
            </div>

            <div className="glass-card">
              <form onSubmit={handleSaveProfile} style={{ display: 'flex', flexDirection: 'column', gap: '24px' }}>
                <div>
                  <label>Net Monthly Income ($)</label>
                  <input 
                    type="number" 
                    placeholder="e.g. 5000" 
                    required 
                    value={profileForm.monthly_income}
                    onChange={e => setProfileForm({...profileForm, monthly_income: e.target.value})}
                  />
                </div>
                <div>
                  <label>Monthly Core Expenses ($)</label>
                  <input 
                    type="number" 
                    placeholder="e.g. 2000" 
                    required 
                    value={profileForm.monthly_expenses}
                    onChange={e => setProfileForm({...profileForm, monthly_expenses: e.target.value})}
                  />
                </div>
                <div>
                  <label>Other Existing Debts ($)</label>
                  <input 
                    type="number" 
                    placeholder="e.g. 300" 
                    required 
                    value={profileForm.existing_debts}
                    onChange={e => setProfileForm({...profileForm, existing_debts: e.target.value})}
                  />
                </div>

                {profileMsg && (
                  <div style={{ background: 'rgba(16, 185, 129, 0.1)', color: 'var(--color-success)', border: '1px solid rgba(16, 185, 129, 0.2)', padding: '12px', borderRadius: '8px', fontSize: '0.9rem' }}>
                    {profileMsg}
                  </div>
                )}

                <button className="bg-gradient-btn" type="submit">
                  Save & Evaluate Health Score
                </button>
              </form>
            </div>
          </div>
        )}

        {/* TAB 3: LOANS MANAGER */}
        {activeTab === 'loans' && (
          <div className="animate-fade-in" style={{ display: 'flex', flexDirection: 'column', gap: '32px' }}>
            <div>
              <h1 style={{ fontSize: '2.2rem', fontWeight: 700 }}>Outstanding Loans</h1>
              <p style={{ color: 'var(--color-text-muted)', marginTop: '4px' }}>Add and manage your active liabilities.</p>
            </div>

            <div style={{ display: 'grid', gridTemplateColumns: '1fr 380px', gap: '32px', alignItems: 'start' }}>
              
              {/* Left Column: Loan Table */}
              <div className="glass-card" style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
                <h3 style={{ fontSize: '1.1rem' }}>Active Liabilities</h3>
                {loans.length > 0 ? (
                  <div style={{ overflowX: 'auto' }}>
                    <table>
                      <thead>
                        <tr>
                          <th>Type</th>
                          <th>Total Loan</th>
                          <th>Outstanding Balance</th>
                          <th>Interest (APR)</th>
                          <th>Due Date</th>
                          <th style={{ textAlign: 'right' }}>Actions</th>
                        </tr>
                      </thead>
                      <tbody>
                        {loans.map((loan) => (
                          <tr key={loan.loan_id}>
                            <td style={{ fontWeight: 600 }}>{loan.loan_type}</td>
                            <td>${parseFloat(loan.loan_amount).toLocaleString(undefined, { minimumFractionDigits: 2 })}</td>
                            <td style={{ color: 'var(--color-danger)', fontWeight: 600 }}>
                              ${parseFloat(loan.outstanding_amount).toLocaleString(undefined, { minimumFractionDigits: 2 })}
                            </td>
                            <td>{loan.interest_rate}%</td>
                            <td>{loan.due_date}</td>
                            <td style={{ display: 'flex', gap: '8px', justifyContent: 'flex-end' }}>
                              <button 
                                className="bg-gradient-accent" 
                                style={{ padding: '6px 12px', fontSize: '0.8rem' }}
                                onClick={() => handleEvaluateSettlement(loan)}
                              >
                                Run AI Analysis
                              </button>
                              <button 
                                className="btn-danger-outline" 
                                style={{ padding: '6px 10px' }}
                                onClick={() => handleDeleteLoan(loan.loan_id)}
                              >
                                <Trash2 size={14} />
                              </button>
                            </td>
                          </tr>
                        ))}
                      </tbody>
                    </table>
                  </div>
                ) : (
                  <p style={{ color: 'var(--color-text-muted)', padding: '20px 0' }}>No loans found. Create your first loan using the form on the right.</p>
                )}
              </div>

              {/* Right Column: Add Loan Form */}
              <div className="glass-card">
                <h3 style={{ marginBottom: '20px', fontSize: '1.1rem' }}>Add Loan Record</h3>
                <form onSubmit={handleAddLoan} style={{ display: 'flex', flexDirection: 'column', gap: '20px' }}>
                  <div>
                    <label>Loan Type</label>
                    <select 
                      value={loanForm.loan_type}
                      onChange={e => setLoanForm({...loanForm, loan_type: e.target.value})}
                    >
                      <option value="Credit Card">Credit Card</option>
                      <option value="Student Loan">Student Loan</option>
                      <option value="Mortgage">Mortgage</option>
                      <option value="Personal Loan">Personal Loan</option>
                      <option value="Auto Loan">Auto Loan</option>
                    </select>
                  </div>
                  <div>
                    <label>Total Borrowed Amount ($)</label>
                    <input 
                      type="number" 
                      placeholder="e.g. 15000" 
                      required 
                      value={loanForm.loan_amount}
                      onChange={e => setLoanForm({...loanForm, loan_amount: e.target.value})}
                    />
                  </div>
                  <div>
                    <label>Outstanding Balance ($)</label>
                    <input 
                      type="number" 
                      placeholder="e.g. 12000" 
                      required 
                      value={loanForm.outstanding_amount}
                      onChange={e => setLoanForm({...loanForm, outstanding_amount: e.target.value})}
                    />
                  </div>
                  <div>
                    <label>Interest Rate (APR %)</label>
                    <input 
                      type="number" 
                      step="0.01" 
                      placeholder="e.g. 18.5" 
                      required 
                      value={loanForm.interest_rate}
                      onChange={e => setLoanForm({...loanForm, interest_rate: e.target.value})}
                    />
                  </div>
                  <div>
                    <label>Due Date</label>
                    <input 
                      type="date" 
                      required 
                      value={loanForm.due_date}
                      onChange={e => setLoanForm({...loanForm, due_date: e.target.value})}
                    />
                  </div>

                  {loanError && (
                    <div style={{ color: 'var(--color-danger)', fontSize: '0.85rem' }}>{loanError}</div>
                  )}

                  <button className="bg-gradient-btn" type="submit">
                    <Plus size={18} />
                    <span>Save Loan</span>
                  </button>
                </form>
              </div>

            </div>
          </div>
        )}

        {/* TAB 4: AI NEGOTIATION */}
        {activeTab === 'negotiation' && (
          <div className="animate-fade-in" style={{ display: 'flex', flexDirection: 'column', gap: '32px' }}>
            <div>
              <h1 style={{ fontSize: '2.2rem', fontWeight: 700 }}>AI Settlement Center</h1>
              <p style={{ color: 'var(--color-text-muted)', marginTop: '4px' }}>Review predictive probabilities and compile legal negotiation letters.</p>
            </div>

            <div style={{ display: 'grid', gridTemplateColumns: '380px 1fr', gap: '32px', alignItems: 'start' }}>
              
              {/* Left Column: Settlement evaluations list */}
              <div className="glass-card" style={{ display: 'flex', flexDirection: 'column', gap: '20px' }}>
                <h3 style={{ fontSize: '1.1rem' }}>Active Risk Reports</h3>
                {settlements.length > 0 ? (
                  <div style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
                    {settlements.map((s) => {
                      const associatedLoan = loans.find(l => l.loan_id === s.loan_id);
                      return (
                        <div 
                          key={s.settlement_id} 
                          onClick={() => setSelectedLoan(associatedLoan)}
                          style={{ 
                            padding: '16px', 
                            background: selectedLoan?.loan_id === s.loan_id ? 'var(--color-primary-glow)' : 'rgba(255,255,255,0.02)', 
                            border: '1px solid',
                            borderColor: selectedLoan?.loan_id === s.loan_id ? 'var(--color-primary)' : 'var(--border-color)',
                            borderRadius: '10px',
                            cursor: 'pointer',
                            transition: 'all 0.2s'
                          }}
                        >
                          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                            <span style={{ fontWeight: 600 }}>{associatedLoan?.loan_type || 'Unknown Debt'}</span>
                            <span className={`badge ${s.priority_level === 'Critical' ? 'badge-danger' : 'badge-warning'}`}>{s.priority_level}</span>
                          </div>
                          <div style={{ marginTop: '12px', display: 'flex', justifyContent: 'space-between', fontSize: '0.85rem' }}>
                            <span style={{ color: 'var(--color-text-muted)' }}>Payoff Target:</span>
                            <span style={{ fontWeight: 700, color: 'var(--color-success)' }}>
                              ${parseFloat(s.recommended_amount).toLocaleString(undefined, { minimumFractionDigits: 2 })}
                            </span>
                          </div>
                          <div style={{ marginTop: '4px', display: 'flex', justifyContent: 'space-between', fontSize: '0.85rem' }}>
                            <span style={{ color: 'var(--color-text-muted)' }}>Possibility:</span>
                            <span>{s.settlement_prediction}</span>
                          </div>
                        </div>
                      );
                    })}
                  </div>
                ) : (
                  <p style={{ color: 'var(--color-text-muted)' }}>No settlement evaluations executed yet. Run an analysis on a loan.</p>
                )}
              </div>

              {/* Right Column: AI Generation Panel */}
              <div className="glass-card" style={{ display: 'flex', flexDirection: 'column', gap: '24px', minHeight: '400px' }}>
                {selectedLoan ? (
                  <>
                    <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', borderBottom: '1px solid var(--border-color)', paddingBottom: '16px' }}>
                      <div>
                        <h3 style={{ fontSize: '1.2rem', fontWeight: 600 }}>Target: {selectedLoan.loan_type}</h3>
                        <p style={{ color: 'var(--color-text-muted)', fontSize: '0.85rem', marginTop: '2px' }}>
                          Outstanding: ${parseFloat(selectedLoan.outstanding_amount).toLocaleString(undefined, { minimumFractionDigits: 2 })} at {selectedLoan.interest_rate}% APR
                        </p>
                      </div>

                      {!negotiationResult && (
                        <button 
                          className="bg-gradient-btn"
                          disabled={isNegotiating}
                          onClick={() => handleGenerateNegotiation(selectedLoan.loan_id)}
                        >
                          <Cpu size={16} />
                          <span>{isNegotiating ? 'Generating Package...' : 'Compile AI Strategy'}</span>
                        </button>
                      )}
                    </div>

                    {negotiationResult ? (
                      <div className="animate-fade-in" style={{ display: 'flex', flexDirection: 'column', gap: '24px' }}>
                        <div>
                          <h4 style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '12px', fontSize: '1rem', color: '#a5b4fc' }}>
                            <TrendingUp size={18} />
                            AI Recommended Negotiation Strategy
                          </h4>
                          <div 
                            style={{ background: 'rgba(0,0,0,0.2)', padding: '20px', borderRadius: '8px', border: '1px solid var(--border-color)', whiteSpace: 'pre-wrap', fontSize: '0.95rem' }}
                          >
                            {negotiationResult.negotiation_strategy}
                          </div>
                        </div>

                        <div>
                          <h4 style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '12px', fontSize: '1rem', color: '#a5b4fc' }}>
                            <FileText size={18} />
                            Generated Hardship Settlement Proposal
                          </h4>
                          <div style={{ position: 'relative' }}>
                            <textarea
                              readOnly
                              rows={15}
                              value={negotiationResult.settlement_letter}
                              style={{ fontFamily: 'monospace', fontSize: '0.85rem', background: '#090d16', color: '#e2e8f0', width: '100%', padding: '20px', borderRadius: '8px', resize: 'none' }}
                            />
                            <button 
                              className="btn-secondary"
                              style={{ position: 'absolute', right: '16px', bottom: '16px', padding: '6px 12px', fontSize: '0.8rem' }}
                              onClick={() => {
                                navigator.clipboard.writeText(negotiationResult.settlement_letter);
                                alert("Settlement letter copied to clipboard!");
                              }}
                            >
                              Copy Letter Text
                            </button>
                          </div>
                        </div>

                        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', fontSize: '0.85rem', color: 'var(--color-text-muted)' }}>
                          <span>Engine: {negotiationResult.ai_response}</span>
                          <button className="btn-secondary" onClick={() => setNegotiationResult(null)}>
                            Reset Negotiation Window
                          </button>
                        </div>
                      </div>
                    ) : (
                      <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', flex: 1, color: 'var(--color-text-muted)' }}>
                        <Cpu size={48} style={{ marginBottom: '16px', opacity: 0.5 }} />
                        <p>Click "Compile AI Strategy" to trigger deep analysis, strategy logging, and document compilation.</p>
                      </div>
                    )}
                  </>
                ) : (
                  <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', flex: 1, color: 'var(--color-text-muted)' }}>
                    <FileText size={48} style={{ marginBottom: '16px', opacity: 0.5 }} />
                    <p>Select an active risk report from the left panel to begin.</p>
                  </div>
                )}
              </div>

            </div>
          </div>
        )}

      </main>
    </div>
  );
}
