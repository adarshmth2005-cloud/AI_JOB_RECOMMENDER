
import { useEffect, useState } from 'react'
import API_BASE_URL from './api'

function Dashboard() {
  const [stats, setStats] = useState({
    total_resumes: 0,
    total_jobs: 0,
    resume_categories: [],
    job_categories: []
  })

  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  useEffect(() => {
    fetch(`${API_BASE_URL}/api/dashboard/stats`)
      .then(response => {
        if (!response.ok) {
          throw new Error('Unable to load dashboard statistics')
        }
        return response.json()
      })
      .then(data => {
        setStats(data.statistics)
        setLoading(false)
      })
      .catch(error => {
        setError(error.message)
        setLoading(false)
      })
  }, [])

  if (loading) {
    return <p>Loading dashboard...</p>
  }

  if (error) {
    return <p>{error}</p>
  }

  return (
    <>
      <section className="welcome">
        <h1>AI Resume Analysis & Job Recommendation</h1>
        <p>
          Analyze your resume, discover your skills
          and find suitable job opportunities.
        </p>
      </section>

      <section className="stats">
        <div className="stat-card">
          <h3>Total Resumes</h3>
          <h1>{stats.total_resumes}</h1>
        </div>

        <div className="stat-card">
          <h3>Total Jobs</h3>
          <h1>{stats.total_jobs}</h1>
        </div>

        <div className="stat-card">
          <h3>Resume Categories</h3>
          <h1>{stats.resume_categories.length}</h1>
        </div>
      </section>

      <section className="info-card">
        <h2>Welcome to Your Dashboard!</h2>
        <p>
          Upload your resume to analyze your skills
          and receive personalized job recommendations.
        </p>
      </section>
    </>
  )
}

export default Dashboard
