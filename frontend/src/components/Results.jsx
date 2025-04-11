import { useState } from "react";
import axios from "axios";

const Results = () => {
  const [result, setResult] = useState(null);

  const fetchSessionData = async () => {
    try {
      const response = await axios.get("http://127.0.0.1:8000/api/session-data/", { withCredentials: true });
      console.log("✅ Fetched Data:", response.data);
      setResult(response.data);
    } catch (error) {
      console.error("❌ Fetch Error:", error);
      setResult({ error: "Failed to fetch data" });
    }
  };

  return (
    <div>
      <span>
        <h2>Stored Data</h2>
      </span>
      <form>
        <input placeholder="enter name" type="text" />
        <input placeholder="enter age" type="text" />
        <input placeholder="enter number" type="text" />
        <input placeholder="enter address" type="text" />
        <input placeholder="enter page" type="text" />

        <button onClick={fetchSessionData}>Fetch Session Data</button>
      </form>

      {result ? (
        <>
          <p><strong>LinkedIn:</strong> {result.linkedin || "Not available"}</p>
          <p><strong>GitHub:</strong> {result.github || "Not available"}</p>
          <p><strong>Resume Text:</strong></p>
          <pre style={{ whiteSpace: "pre-wrap" }}>{result.resume_text || "No resume text stored"}</pre>
        </>
      ) : (
        <p>No data available. Submit a profile or fetch stored data.</p>
      )}

    </div>

  );
};

export default Results;
