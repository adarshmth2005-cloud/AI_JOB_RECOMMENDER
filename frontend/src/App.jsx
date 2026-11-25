
import { useState } from 'react'
import './App.css'

import Dashboard from './Dashboard'
import ResumeUpload from './ResumeUpload'
import ResumeAnalysis from './ResumeAnalysis'
import JobRecommendations from './JobRecommendations'

const API = 'http://127.0.0.1:5000'

function App() {
  const [token, setToken] = useState(
    () => localStorage.getItem('authToken') || ''
  )

  const [user, setUser] = useState(() => {
    try {
      return JSON.parse(localStorage.getItem('authUser') || 'null')
    } catch {
      return null
    }
  })

  const [activePage, setActivePage] = useState('Dashboard')
  const [authPage, setAuthPage] = useState('login')

  const [name, setName] = useState('')
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')

  const [loading, setLoading] = useState(false)
  const [message, setMessage] = useState('')
  const [messageType, setMessageType] = useState('error')

  const handleAuth = async (e) => {
    e.preventDefault()
    setMessage('')
    setLoading(true)

    const endpoint =
      authPage === 'register' ? 'register' : 'login'

    const body =
      authPage === 'register'
        ? { name, email, password }
        : { email, password }

    try {
      const response = await fetch(`${API}/api/auth/${endpoint}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(body),
      })

      const data = await response.json()

      if (!response.ok) {
        throw new Error(data.message || 'Request failed.')
      }

      if (authPage === 'register') {
        setMessage('Registration successful! Please login.')
        setMessageType('success')
        setAuthPage('login')
        setName('')
        setPassword('')
      } else {
        localStorage.setItem('authToken', data.token)
        localStorage.setItem('authUser', JSON.stringify(data.user))

        setToken(data.token)
        setUser(data.user)
        setActivePage('Dashboard')
        setEmail('')
        setPassword('')
        setMessage('')
      }
    } catch (error) {
      setMessage(error.message || 'Something went wrong.')
      setMessageType('error')
    } finally {
      setLoading(false)
    }
  }

  const handleLogout = async () => {
    try {
      await fetch(`${API}/api/auth/logout`, {
        method: 'POST',
      })
    } catch {
      // Local logout will still continue.
    }

    localStorage.removeItem('authToken')
    localStorage.removeItem('authUser')

    setToken('')
    setUser(null)
    setActivePage('Dashboard')
    setAuthPage('login')
    setMessage('')
  }

  // Login and Registration screen
  if (!token) {
    return (
      <div className="auth-page">
        <div className="auth-card">
          <h1>AI Job Finder</h1>

          <p className="auth-subtitle">
            AI-Based Resume Analysis and Job Recommendation System
          </p>

          <div className="auth-tabs">
            <button
              type="button"
              className={authPage === 'login' ? 'auth-tab active' : 'auth-tab'}
              onClick={() => {
                setAuthPage('login')
                setMessage('')
              }}
            >
              Login
            </button>

            <button
              type="button"
              className={authPage === 'register' ? 'auth-tab active' : 'auth-tab'}
              onClick={() => {
                setAuthPage('register')
                setMessage('')
              }}
            >
              Register
            </button>
          </div>

          <h2>
            {authPage === 'login' ? 'Welcome Back' : 'Create Account'}
          </h2>

          <form onSubmit={handleAuth}>
            {authPage === 'register' && (
              <div className="auth-field">
                <label>Full Name</label>
                <input
                  type="text"
                  placeholder="Enter your name"
                  value={name}
                  onChange={(e) => setName(e.target.value)}
                  required
                />
              </div>
            )}

            <div className="auth-field">
              <label>Email Address</label>
              <input
                type="email"
                placeholder="Enter your email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                required
              />
            </div>

            <div className="auth-field">
              <label>Password</label>
              <input
                type="password"
                placeholder="Minimum 8 characters"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                minLength={8}
                required
              />
            </div>

            {message && (
              <p
                className={
                  messageType === 'success'
                    ? 'auth-message success'
                    : 'auth-message error'
                }
              >
                {message}
              </p>
            )}

            <button
              type="submit"
              className="auth-submit"
              disabled={loading}
            >
              {loading
                ? 'Please wait...'
                : authPage === 'login'
                  ? 'Login'
                  : 'Create Account'}
            </button>
          </form>

          <p className="auth-footer">
            {authPage === 'login'
              ? "Don't have an account? Register here."
              : 'Already have an account? Login here.'}
          </p>
        </div>
      </div>
    )
  }

  return (
    <div className="app">
      {/* Sidebar */}
      <aside className="sidebar">
        <h2>AI Job Finder</h2>

        <nav>
          {[
            'Dashboard',
            'Upload Resume',
            'Resume Analysis',
            'Job Recommendations',
          ].map((page) => (
            <p
              key={page}
              className={activePage === page ? 'active' : ''}
              onClick={() => setActivePage(page)}
            >
              {page}
            </p>
          ))}
        </nav>
      </aside>

      {/* Main Content */}
      <main className="main-content">
        <header className="topbar">
          <div>
            <h2>{activePage}</h2>
            <span>Welcome to AI Job Finder</span>
          </div>

          <div className="user-menu">
            <span>{user?.name || user?.email || 'User'}</span>

            <button type="button" onClick={handleLogout}>
              Logout
            </button>
          </div>
        </header>

        {activePage === 'Dashboard' && <Dashboard />}

        {activePage === 'Upload Resume' && <ResumeUpload />}

        {activePage === 'Resume Analysis' && <ResumeAnalysis />}

        {activePage === 'Job Recommendations' && (
          <JobRecommendations />
        )}
      </main>
    </div>
  )
}

export default App
