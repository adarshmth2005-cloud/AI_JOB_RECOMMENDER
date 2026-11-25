
import { useEffect, useState } from 'react'
import API_BASE_URL from './api'

function ResumeUpload() {
  const [file, setFile] = useState(null)
  const [previewUrl, setPreviewUrl] = useState('')
  const [message, setMessage] = useState('')
  const [loading, setLoading] = useState(false)

  useEffect(() => {
    if (!file) {
      setPreviewUrl('')
      return
    }

    const url = URL.createObjectURL(file)
    setPreviewUrl(url)

    return () => URL.revokeObjectURL(url)
  }, [file])

  const handleUpload = async () => {
    if (!file) {
      setMessage('Please select a PDF resume first.')
      return
    }

    const formData = new FormData()
    formData.append('resume', file)

    try {
      setLoading(true)
      setMessage('Uploading resume...')

      const response = await fetch(
        `${API_BASE_URL}/api/resumes/upload`,
        {
          method: 'POST',
          body: formData
        }
      )

      const data = await response.json()

      if (!response.ok) {
        throw new Error(data.message || 'Upload failed')
      }

      setMessage(data.message || 'Resume uploaded and analyzed successfully!')
    } catch (error) {
      setMessage(error.message || 'Something went wrong.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="upload-card">
      <h2>Upload Your Resume</h2>
      <p>Select your resume in PDF format.</p>

      <input
        type="file"
        accept=".pdf,application/pdf"
        onChange={e => {
          setFile(e.target.files[0] || null)
          setMessage('')
        }}
      />

      {file && <p>Selected file: {file.name}</p>}

      <button onClick={handleUpload} disabled={loading}>
        {loading ? 'Uploading...' : 'Upload Resume'}
      </button>

      {message && <p>{message}</p>}

      {previewUrl && (
        <div className="resume-preview">
          <h3>Your Resume Preview</h3>
          <iframe
            src={previewUrl}
            title="Resume Preview"
            width="100%"
            height="600px"
            style={{
              border: '1px solid #cbd5e1',
              borderRadius: '8px',
              marginTop: '15px'
            }}
          />
        </div>
      )}
    </div>
  )
}

export default ResumeUpload
