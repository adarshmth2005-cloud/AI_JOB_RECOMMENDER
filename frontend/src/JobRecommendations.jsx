
import { useEffect, useRef, useState } from 'react'

const API = 'http://127.0.0.1:5000/api'
const JOBS_PER_PAGE = 50

function JobRecommendations() {
  const [resumes, setResumes] = useState([])
  const [resumeId, setResumeId] = useState('')
  const [resumeCursor, setResumeCursor] = useState(null)
  const [hasMoreResumes, setHasMoreResumes] = useState(false)

  const [categories, setCategories] = useState([])
  const [locations, setLocations] = useState([])

  const [category, setCategory] = useState('')
  const [location, setLocation] = useState('')

  const [jobs, setJobs] = useState([])
  const [totalJobs, setTotalJobs] = useState(0)
  const [page, setPage] = useState(1)
  const [hasMoreJobs, setHasMoreJobs] = useState(false)

  const [message, setMessage] = useState('Loading data...')
  const [loading, setLoading] = useState(false)
  const [loadingResumes, setLoadingResumes] = useState(false)

  const resumeLoadingRef = useRef(false)
  const jobLoadingRef = useRef(false)

  // Load resumes
  const loadResumes = async (nextCursor = null) => {
    if (resumeLoadingRef.current) return

    resumeLoadingRef.current = true
    setLoadingResumes(true)

    try {
      let url = `${API}/resumes/?limit=50`

      if (nextCursor) {
        url += `&cursor=${nextCursor}`
      }

      const response = await fetch(url)

      if (!response.ok) {
        throw new Error('Unable to load resumes')
      }

      const data = await response.json()
      const newResumes = data.resumes || []

      setResumes(previous => {
        const combined = nextCursor
          ? [...previous, ...newResumes]
          : newResumes

        return Array.from(
          new Map(combined.map(item => [item.id, item])).values()
        )
      })

      setResumeCursor(data.next_cursor || null)
      setHasMoreResumes(Boolean(data.has_more))

      setMessage(
        newResumes.length
          ? ''
          : 'No resumes found. Please upload a resume first.'
      )
    } catch (error) {
      setMessage(error.message)
    } finally {
      setLoadingResumes(false)
      resumeLoadingRef.current = false
    }
  }

  // Load categories and locations
  useEffect(() => {
    loadResumes()

    const loadFilters = async () => {
      try {
        const [categoryResponse, locationResponse] = await Promise.all([
          fetch(`${API}/jobs/categories`),
          fetch(`${API}/jobs/locations`)
        ])

        if (!categoryResponse.ok || !locationResponse.ok) {
          throw new Error('Unable to load job filters')
        }

        const categoryData = await categoryResponse.json()
        const locationData = await locationResponse.json()

        setCategories(categoryData.categories || [])
        setLocations(locationData.locations || [])
      } catch (error) {
        setMessage(error.message)
      }
    }

    loadFilters()
  }, [])

  // Fetch recommendations
  const fetchRecommendations = async (requestedPage, append = false) => {
    if (!resumeId) {
      setMessage('Please select a resume first.')
      return
    }

    if (jobLoadingRef.current) return

    jobLoadingRef.current = true
    setLoading(true)

    if (!append) {
      setJobs([])
      setTotalJobs(0)
      setPage(1)
      setHasMoreJobs(false)
      setMessage('Finding matching jobs...')
    }

    try {
      const params = new URLSearchParams()

      params.append('page', String(requestedPage))
      params.append('per_page', String(JOBS_PER_PAGE))

      if (category) params.append('category', category)
      if (location) params.append('location', location)

      const response = await fetch(
        `${API}/recommendations/${resumeId}?${params.toString()}`
      )

      const data = await response.json()

      if (!response.ok) {
        throw new Error(data.message || 'Could not get recommendations')
      }

      const results = data.recommendations || []

      setJobs(previous =>
        append ? [...previous, ...results] : results
      )

      setTotalJobs(data.total_recommendations || 0)
      setPage(data.current_page || requestedPage)
      setHasMoreJobs(Boolean(data.has_more))

      setMessage(
        data.total_recommendations > 0
          ? ''
          : 'No matching jobs found.'
      )
    } catch (error) {
      setMessage(error.message)
    } finally {
      setLoading(false)
      jobLoadingRef.current = false
    }
  }

  // Find jobs
  const getRecommendations = () => {
    fetchRecommendations(1, false)
  }

  // Load more jobs
  const loadMoreJobs = () => {
    if (hasMoreJobs && !loading) {
      fetchRecommendations(page + 1, true)
    }
  }

  // Job card with company, location and email links
  const renderJobCard = job => {
    const company = job.company || ''
    const jobLocation = job.location || ''

    const companySearchUrl = company
      ? `https://www.google.com/search?q=${encodeURIComponent(
          company + ' official website'
        )}`
      : '#'

    const locationMapUrl = jobLocation
      ? `https://www.google.com/maps/search/?api=1&query=${encodeURIComponent(
          jobLocation
        )}`
      : '#'

    const emailSearchUrl = company
      ? `https://www.google.com/search?q=${encodeURIComponent(
          company + ' official contact email'
        )}`
      : '#'

    return (
      <div className="stat-card" key={job.job_id}>
        <h3>{job.job_title}</h3>

        <p>
          <strong>Company:</strong>{' '}
          {company ? (
            <a
              href={companySearchUrl}
              target="_blank"
              rel="noopener noreferrer"
            >
              {company}
            </a>
          ) : (
            'Not specified'
          )}
        </p>

        <p>
          <strong>Location:</strong>{' '}
          {jobLocation ? (
            <a
              href={locationMapUrl}
              target="_blank"
              rel="noopener noreferrer"
            >
              {jobLocation}
            </a>
          ) : (
            'Not specified'
          )}
        </p>

        <p>
          <strong>Category:</strong>{' '}
          {job.job_category || 'Not specified'}
        </p>

        <p>
          <strong>Company Email:</strong>{' '}
          {company ? (
            <a
              href={emailSearchUrl}
              target="_blank"
              rel="noopener noreferrer"
            >
              Find Official Email
            </a>
          ) : (
            'Not available'
          )}
        </p>
      </div>
    )
  }

  return (
    <div className="info-card">
      <h2>Job Recommendations</h2>

      <p>Find jobs according to your resume skills.</p>

      {/* Resume selection */}
      <div style={{ marginTop: '15px' }}>
        <label
          htmlFor="resume-select"
          style={{ display: 'block', marginBottom: '8px' }}
        >
          Select Resume
        </label>

        <select
          id="resume-select"
          value={resumeId}
          onChange={e => {
            setResumeId(e.target.value)
            setJobs([])
            setTotalJobs(0)
            setPage(1)
            setHasMoreJobs(false)
            setMessage('')
          }}
        >
          <option value="">Select Resume</option>

          {resumes.map(resume => (
            <option key={resume.id} value={resume.id}>
              {resume.filename || `Resume ${resume.id}`} (ID: {resume.id})
            </option>
          ))}
        </select>
      </div>

      <p style={{ marginTop: '8px' }}>
        Loaded resumes: {resumes.length}
      </p>

      {hasMoreResumes && (
        <button
          type="button"
          onClick={() => loadResumes(resumeCursor)}
          disabled={loadingResumes}
        >
          {loadingResumes ? 'Loading...' : 'Load More Resumes'}
        </button>
      )}

      {/* Job category */}
      <div style={{ marginTop: '15px' }}>
        <label
          htmlFor="job-category"
          style={{ display: 'block', marginBottom: '8px' }}
        >
          Job Category
        </label>

        <select
          id="job-category"
          value={category}
          onChange={e => setCategory(e.target.value)}
        >
          <option value="">All Categories</option>

          {categories.map(item => (
            <option key={item} value={item}>
              {item}
            </option>
          ))}
        </select>
      </div>

      {/* Job location */}
      <div style={{ marginTop: '15px' }}>
        <label
          htmlFor="job-location"
          style={{ display: 'block', marginBottom: '8px' }}
        >
          Job Location
        </label>

        <select
          id="job-location"
          value={location}
          onChange={e => setLocation(e.target.value)}
        >
          <option value="">All Locations</option>

          {locations.map(item => (
            <option key={item} value={item}>
              {item}
            </option>
          ))}
        </select>
      </div>

      {/* Find matching jobs */}
      <button
        type="button"
        onClick={getRecommendations}
        disabled={loading}
        style={{ marginTop: '15px' }}
      >
        {loading ? 'Searching...' : 'Find Matching Jobs'}
      </button>

      {message && (
        <p style={{ marginTop: '15px' }}>
          {message}
        </p>
      )}

      {/* Only job cards */}
      {jobs.length > 0 && (
        <>
          <h3 style={{ marginTop: '20px' }}>
            Total Matching Jobs: {totalJobs}
          </h3>

          <p>Loaded Jobs: {jobs.length}</p>

          <div>
            {jobs.map(renderJobCard)}
          </div>

          {hasMoreJobs && (
            <button
              type="button"
              onClick={loadMoreJobs}
              disabled={loading}
              style={{ marginTop: '20px' }}
            >
              {loading ? 'Loading Jobs...' : 'Load More Jobs'}
            </button>
          )}
        </>
      )}
    </div>
  )
}

export default JobRecommendations
