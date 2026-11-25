
import { useEffect, useRef, useState } from "react";

const API = "http://127.0.0.1:5000";

function ResumeAnalysis() {
  const [resumes, setResumes] = useState([]);
  const [selectedId, setSelectedId] = useState("");
  const [analysis, setAnalysis] = useState(null);

  const [search, setSearch] = useState("");
  const [showList, setShowList] = useState(false);

  const [cursor, setCursor] = useState(null);
  const [hasMore, setHasMore] = useState(false);

  const [loadingResumes, setLoadingResumes] = useState(false);
  const [loadingAnalysis, setLoadingAnalysis] = useState(false);
  const [message, setMessage] = useState("");

  const [pdfAvailable, setPdfAvailable] = useState(false);
  const [pdfChecked, setPdfChecked] = useState(false);

  // Job selection and skills comparison
  const [jobs, setJobs] = useState([]);
  const [selectedJobId, setSelectedJobId] = useState("");
  const [skillComparison, setSkillComparison] = useState(null);
  const [loadingJobs, setLoadingJobs] = useState(false);
  const [loadingComparison, setLoadingComparison] = useState(false);
  const [comparisonMessage, setComparisonMessage] = useState("");

  const loadingRef = useRef(false);

  // Load resumes from backend
  const loadResumes = async (reset = false, searchValue = search) => {
    if (loadingRef.current) return;

    loadingRef.current = true;
    setLoadingResumes(true);
    setMessage("");

    try {
      const nextCursor = reset ? null : cursor;

      const params = new URLSearchParams();
      params.append("limit", "50");

      if (searchValue.trim()) {
        params.append("search", searchValue.trim());
      }

      if (nextCursor && !reset) {
        params.append("cursor", String(nextCursor));
      }

      const response = await fetch(
        `${API}/api/resumes/?${params.toString()}`
      );

      const data = await response.json();

      if (!response.ok) {
        throw new Error(
          data.message || "Resumes load nahi ho sake."
        );
      }

      const newResumes = data.resumes || [];

      setResumes((previous) => {
        if (reset) return newResumes;

        const combined = [...previous, ...newResumes];

        return Array.from(
          new Map(
            combined.map((resume) => [resume.id, resume])
          ).values()
        );
      });

      setCursor(data.next_cursor || null);
      setHasMore(Boolean(data.has_more));

      if (newResumes.length === 0) {
        setMessage(
          searchValue.trim()
            ? "Koi matching resume nahi mila."
            : "Abhi koi resume available nahi hai."
        );
      }
    } catch (error) {
      setMessage(error.message);
    } finally {
      setLoadingResumes(false);
      loadingRef.current = false;
    }
  };

  // Load jobs from backend
  const loadJobs = async () => {
    setLoadingJobs(true);

    try {
      const response = await fetch(
        `${API}/api/jobs/?limit=100`
      );

      const data = await response.json();

      if (!response.ok) {
        throw new Error(
          data.message || "Jobs load nahi ho sake."
        );
      }

      setJobs(data.jobs || []);
    } catch (error) {
      setComparisonMessage(error.message);
    } finally {
      setLoadingJobs(false);
    }
  };

  // Load jobs when component opens
  useEffect(() => {
    loadJobs();
  }, []);

  // Select Resume button
  const handleShowList = () => {
    setShowList(true);
    loadResumes(true, search);
  };

  // Search directly from backend
  const handleSearch = (value) => {
    setSearch(value);
    setShowList(true);
  };

  // Search after user stops typing
  useEffect(() => {
    if (!showList) return;

    const timer = setTimeout(() => {
      loadResumes(true, search);
    }, 400);

    return () => clearTimeout(timer);
  }, [search, showList]);

  // Select resume and get analysis
  const handleSelectResume = async (resumeId) => {
    setSelectedId(resumeId);
    setAnalysis(null);
    setPdfAvailable(false);
    setPdfChecked(false);
    setSkillComparison(null);
    setSelectedJobId("");
    setComparisonMessage("");
    setMessage("");
    setShowList(false);

    setLoadingAnalysis(true);

    try {
      const response = await fetch(
        `${API}/api/resumes/${resumeId}/analysis`
      );

      const data = await response.json();

      if (!response.ok) {
        throw new Error(
          data.message || "Resume analysis nahi mil saka."
        );
      }

      setAnalysis(data.analysis || data);

      // Check whether PDF is available
      const pdfResponse = await fetch(
        `${API}/api/resumes/${resumeId}/file`,
        { method: "GET" }
      );

      setPdfAvailable(pdfResponse.ok);
      setPdfChecked(true);

      if (pdfResponse.body) {
        await pdfResponse.body.cancel();
      }
    } catch (error) {
      setMessage(error.message);
    } finally {
      setLoadingAnalysis(false);
    }
  };

  // Compare resume skills with selected job
  const handleCompareSkills = async () => {
    if (!selectedId) {
      setComparisonMessage("Please select a resume first.");
      return;
    }

    if (!selectedJobId) {
      setComparisonMessage("Please select a job first.");
      return;
    }

    setLoadingComparison(true);
    setSkillComparison(null);
    setComparisonMessage("");

    try {
      const response = await fetch(
        `${API}/api/resumes/${selectedId}/missing-skills/${selectedJobId}`
      );

      const data = await response.json();

      if (!response.ok) {
        throw new Error(
          data.message || "Skills comparison nahi ho saka."
        );
      }

      setSkillComparison(data);
    } catch (error) {
      setComparisonMessage(error.message);
    } finally {
      setLoadingComparison(false);
    }
  };

  // Hide search list
  const handleClearSearch = () => {
    setSearch("");
    setShowList(false);
    setResumes([]);
    setCursor(null);
    setHasMore(false);
    setMessage("");
  };

  return (
    <div className="resume-analysis-page">
      <h2>Resume Analyzer</h2>

      <p>
        Search ya select karke uploaded resume ka analysis,
        skills aur PDF dekhein.
      </p>

      {/* Search section */}
      <div style={{ marginTop: "20px", marginBottom: "20px" }}>
        <label
          htmlFor="resume-search"
          style={{ display: "block", marginBottom: "8px" }}
        >
          Search Resume
        </label>

        <input
          id="resume-search"
          type="text"
          placeholder="Search by resume name or ID..."
          value={search}
          onChange={(e) => handleSearch(e.target.value)}
          style={{
            width: "100%",
            maxWidth: "500px",
            padding: "12px",
            border: "1px solid #ccc",
            borderRadius: "6px",
          }}
        />

        <div style={{ marginTop: "10px" }}>
          <button
            type="button"
            onClick={handleShowList}
            style={{
              padding: "12px 18px",
              cursor: "pointer",
            }}
          >
            Select Resume
          </button>

          {(search || showList) && (
            <button
              type="button"
              onClick={handleClearSearch}
              style={{
                padding: "12px 18px",
                marginLeft: "10px",
                cursor: "pointer",
              }}
            >
              Hide List
            </button>
          )}
        </div>
      </div>

      {message && (
        <p style={{ color: "red", margin: "12px 0" }}>
          {message}
        </p>
      )}

      {/* Resume list */}
      {showList && (
        <div
          style={{
            border: "1px solid #ddd",
            borderRadius: "8px",
            padding: "15px",
            marginBottom: "25px",
            maxHeight: "450px",
            overflowY: "auto",
          }}
        >
          <h3>Available Resumes</h3>

          {loadingResumes && <p>Searching resumes...</p>}

          {!loadingResumes && resumes.length === 0 && (
            <p>
              {search
                ? "Koi matching resume nahi mila."
                : "Abhi koi resume available nahi hai."}
            </p>
          )}

          {resumes.map((resume) => (
            <div
              key={resume.id}
              onClick={() => handleSelectResume(resume.id)}
              style={{
                padding: "12px",
                marginTop: "10px",
                border: "1px solid #ddd",
                borderRadius: "6px",
                cursor: "pointer",
                background:
                  String(selectedId) === String(resume.id)
                    ? "#e8f0fe"
                    : "#fff",
              }}
            >
              <strong>
                {resume.filename || `Resume ${resume.id}`}
              </strong>

              <p>ID: {resume.id}</p>

              <p>
                Category: {resume.category || "Not classified"}
              </p>
            </div>
          ))}

          {hasMore && (
            <button
              type="button"
              onClick={() => loadResumes(false, search)}
              disabled={loadingResumes}
              style={{
                padding: "10px 16px",
                marginTop: "15px",
                cursor: "pointer",
              }}
            >
              {loadingResumes ? "Loading..." : "Load More Resumes"}
            </button>
          )}
        </div>
      )}

      {/* Analysis section */}
      {loadingAnalysis && <p>Analyzing resume...</p>}

      {analysis && (
        <div style={{ marginTop: "25px" }}>
          <h3>Resume Analysis</h3>

          <p>
            <strong>Selected Resume ID:</strong> {selectedId}
          </p>

          <p>
            <strong>Category:</strong>{" "}
            {analysis.category || "Not classified"}
          </p>

          <p>
            <strong>Text Length:</strong>{" "}
            {analysis.text_length || 0}
          </p>

          <h4 style={{ marginTop: "15px" }}>
            Extracted Skills
          </h4>

          {analysis.skills && analysis.skills.length > 0 ? (
            <div style={{ marginTop: "8px" }}>
              {Array.isArray(analysis.skills)
                ? analysis.skills.map((skill, index) => (
                    <span
                      key={index}
                      style={{
                        display: "inline-block",
                        padding: "6px 10px",
                        margin: "4px",
                        background: "#e8f0fe",
                        borderRadius: "15px",
                      }}
                    >
                      {skill}
                    </span>
                  ))
                : analysis.skills}
            </div>
          ) : (
            <p>No skills found.</p>
          )}

          {/* Job skills comparison */}
          <div
            style={{
              marginTop: "25px",
              padding: "18px",
              border: "1px solid #ddd",
              borderRadius: "8px",
            }}
          >
            <h3>Job Skills Comparison</h3>

            <p style={{ marginTop: "8px" }}>
              Select a job to compare its required skills with this resume.
            </p>

            <label
              htmlFor="job-select"
              style={{
                display: "block",
                marginTop: "15px",
                marginBottom: "8px",
              }}
            >
              Select Job
            </label>

            <select
              id="job-select"
              value={selectedJobId}
              onChange={(e) => {
                setSelectedJobId(e.target.value);
                setSkillComparison(null);
                setComparisonMessage("");
              }}
              style={{
                width: "100%",
                maxWidth: "500px",
                padding: "10px",
                border: "1px solid #ccc",
                borderRadius: "6px",
              }}
            >
              <option value="">Select a job</option>

              {jobs.map((job) => (
                <option key={job.id} value={job.id}>
                  {job.title} - {job.company}
                </option>
              ))}
            </select>

            {loadingJobs && <p>Loading jobs...</p>}

            {!loadingJobs && jobs.length === 0 && (
              <p>No jobs available.</p>
            )}

            <div style={{ marginTop: "15px" }}>
              <button
                type="button"
                onClick={handleCompareSkills}
                disabled={loadingComparison || !selectedJobId}
                style={{
                  padding: "11px 18px",
                  cursor: "pointer",
                }}
              >
                {loadingComparison
                  ? "Comparing..."
                  : "Compare Skills"}
              </button>
            </div>

            {comparisonMessage && (
              <p style={{ color: "red", marginTop: "12px" }}>
                {comparisonMessage}
              </p>
            )}

            {skillComparison && (
              <div style={{ marginTop: "20px" }}>
                <h4>Matched Skills</h4>

                {skillComparison.matched_skills?.length > 0 ? (
                  <div style={{ marginTop: "8px" }}>
                    {skillComparison.matched_skills.map(
                      (skill, index) => (
                        <span
                          key={index}
                          style={{
                            display: "inline-block",
                            padding: "7px 11px",
                            margin: "4px",
                            background: "#dcfce7",
                            color: "#166534",
                            borderRadius: "15px",
                          }}
                        >
                          {skill}
                        </span>
                      )
                    )}
                  </div>
                ) : (
                  <p>No matched skills found.</p>
                )}

                <h4 style={{ marginTop: "20px" }}>
                  Missing Skills
                </h4>

                {skillComparison.missing_skills?.length > 0 ? (
                  <div style={{ marginTop: "8px" }}>
                    {skillComparison.missing_skills.map(
                      (skill, index) => (
                        <span
                          key={index}
                          style={{
                            display: "inline-block",
                            padding: "7px 11px",
                            margin: "4px",
                            background: "#fee2e2",
                            color: "#991b1b",
                            borderRadius: "15px",
                          }}
                        >
                          {skill}
                        </span>
                      )
                    )}
                  </div>
                ) : (
                  <p>No missing skills found.</p>
                )}
              </div>
            )}
          </div>

          <h4 style={{ marginTop: "20px" }}>
            Extracted Resume Text
          </h4>

          <div
            style={{
              padding: "12px",
              background: "#f5f5f5",
              borderRadius: "6px",
              whiteSpace: "pre-wrap",
              maxHeight: "300px",
              overflowY: "auto",
              marginTop: "8px",
            }}
          >
            {analysis.extracted_text ||
              "No extracted text available."}
          </div>

          <h3 style={{ marginTop: "25px" }}>
            Resume PDF
          </h3>

          {pdfChecked && pdfAvailable && (
            <iframe
              title="Resume PDF"
              src={`${API}/api/resumes/${selectedId}/file`}
              width="100%"
              height="600px"
              style={{
                border: "1px solid #ccc",
                borderRadius: "8px",
                marginTop: "10px",
              }}
            />
          )}

          {pdfChecked && !pdfAvailable && (
            <p style={{ marginTop: "10px" }}>
              Original PDF Not Available. Is resume ka text
              database mein available hai, lekin original PDF
              file server par nahi mili.
            </p>
          )}
        </div>
      )}
    </div>
  );
}

export default ResumeAnalysis;
