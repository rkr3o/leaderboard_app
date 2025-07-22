import React, { useState, useEffect } from "react";

function Leaderboard() {
  const [token, setToken] = useState(null);
  const [leaderboard, setLeaderboard] = useState([]);
  const [searchUserId, setSearchUserId] = useState("");
  const [searchedRank, setSearchedRank] = useState(null);
  const [error, setError] = useState("");
  const [loadingToken, setLoadingToken] = useState(false);
  const [loadingRank, setLoadingRank] = useState(false);

  // Fetch JWT token once on component mount for default user_id=1
  useEffect(() => {
    const fetchToken = async () => {
      setLoadingToken(true);
      try {
        const res = await fetch("http://127.0.0.1:8000/api/user/token/", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({ user_id: 1 }), // hardcoded or get from config
        });

        if (!res.ok) {
          const errData = await res.json();
          throw new Error(errData.error || "Failed to get token");
        }

        const data = await res.json();
        setToken(data.token); // Assuming response shape { token: "..." }
        setError("");
      } catch (err) {
        setError(err.message);
        setToken(null);
      } finally {
        setLoadingToken(false);
      }
    };

    fetchToken();
  }, []); // empty deps → run once

  // Poll leaderboard every 5 sec after token is available
  useEffect(() => {
    if (!token) return;

    const fetchLeaderboard = async () => {
      try {
        const res = await fetch("http://127.0.0.1:8000/api/leaderboard/top/", {
          headers: {
            Authorization: token,
            "Content-Type": "application/json",
          },
        });

        if (!res.ok) throw new Error("Failed to fetch leaderboard");

        const data = await res.json();
        setLeaderboard(data);
      } catch (err) {
        setError(err.message);
      }
    };

    fetchLeaderboard();
    const interval = setInterval(fetchLeaderboard, 5000);

    return () => clearInterval(interval);
  }, [token]);

  // Fetch user rank on button click
  const handleSearchRank = async () => {
    if (!searchUserId) {
      setError("Please enter a User ID");
      setSearchedRank(null);
      return;
    }
    if (!token) {
      setError("No auth token available");
      return;
    }

    setLoadingRank(true);
    try {
      const res = await fetch(
        `http://127.0.0.1:8000/api/leaderboard/rank?user_id=${searchUserId}`,
        {
          headers: {
            Authorization: token,
            "Content-Type": "application/json",
          },
        }
      );

      if (!res.ok) {
        if (res.status === 404) {
          setError("No leaderboard entry found for this user.");
          setSearchedRank(null);
        } else {
          const errData = await res.json();
          setError(errData.error || "Failed to fetch user rank");
          setSearchedRank(null);
        }
        return;
      }

      const data = await res.json();
      setSearchedRank(data.rank);
      setError("");
    } catch (err) {
      setError(err.message);
      setSearchedRank(null);
    } finally {
      setLoadingRank(false);
    }
  };

  return (
    <div style={{ maxWidth: 600, margin: "auto", padding: 20 }}>
      <h1>Game Leaderboard</h1>

      {loadingToken ? (
        <p>Fetching auth token...</p>
      ) : error ? (
        <p style={{ color: "red" }}>{error}</p>
      ) : null}

      <div style={{ marginBottom: 20 }}>
        <input
          type="number"
          placeholder="Enter User ID"
          value={searchUserId}
          onChange={(e) => setSearchUserId(e.target.value)}
          style={{ width: 150 }}
        />
        <button onClick={handleSearchRank} disabled={loadingRank} style={{ marginLeft: 10 }}>
          {loadingRank ? "Searching..." : "Search Rank"}
        </button>
        {searchedRank !== null && (
          <span style={{ marginLeft: 15, fontWeight: "bold" }}>
            Rank: {searchedRank}
          </span>
        )}
      </div>

      <table
        style={{
          width: "100%",
          borderCollapse: "collapse",
          textAlign: "left",
          fontFamily: "Arial, sans-serif",
        }}
      >
        <thead>
          <tr style={{ borderBottom: "2px solid #ddd" }}>
            <th style={{ padding: "8px" }}>Rank</th>
            <th style={{ padding: "8px" }}>User ID</th>
            <th style={{ padding: "8px" }}>Total Score</th>
          </tr>
        </thead>
        <tbody>
          {leaderboard.length === 0 ? (
            <tr>
              <td colSpan="3" style={{ padding: "8px" }}>
                Loading leaderboard...
              </td>
            </tr>
          ) : (
            leaderboard.map(({ user_id, total_score, rank }) => (
              <tr key={user_id}>
                <td style={{ padding: "8px" }}>{rank}</td>
                <td style={{ padding: "8px" }}>{user_id}</td>
                <td style={{ padding: "8px" }}>{total_score}</td>
              </tr>
            ))
          )}
        </tbody>
      </table>
    </div>
  );
}

export default Leaderboard;
