import { useEffect, useState } from "react";
import axios from "axios";
import Confetti from "react-confetti";

const API_URL = "http://localhost:8000/api";

function App() {
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [userId, setUserId] = useState(null);
  const [isRegistered, setIsRegistered] = useState(false);
  const [question, setQuestion] = useState(null);
  const [selectedAnswer, setSelectedAnswer] = useState(null);
  const [feedback, setFeedback] = useState("");
  const [funFact, setFunFact] = useState("");
  const [correctCount, setCorrectCount] = useState(0);
  const [wrongCount, setWrongCount] = useState(0);
  const [nextButtonText, setNextButtonText] = useState("🔄 Next Question");
  const [showConfetti, setShowConfetti] = useState(false);
  const [showSadFace, setShowSadFace] = useState(false);
  const [loading, setLoading] = useState(false);
  const [inviteLink, setInviteLink] = useState("");
  const [inviteImage, setInviteImage] = useState("");

  useEffect(() => {
    if (isRegistered) {
      fetchQuestion();
    }
  }, [isRegistered]);

  const registerUser = async () => {
    if (!name.trim() || !email.trim() || !password.trim()) return alert("Please enter all details.");
    try {
      const response = await axios.post(`${API_URL}/users/register`, { name, email, password });
      setUserId(response.data.user_id);
      setIsRegistered(true);
      fetchQuestion();
    } catch (error) {
      console.error("Error registering user:", error);
    }
  };

  const fetchQuestion = async () => {
    setLoading(true);
    setSelectedAnswer(null);
    setFeedback("");
    setFunFact("");
    setShowConfetti(false);
    setShowSadFace(false);

    try {
      const response = await axios.post(`${API_URL}/destinations`, {
        category: "travel",
        difficulty: "easy",
        user_id: userId,
        action: "random_destination",
      });
      setQuestion(response.data);
    } catch (error) {
      console.error("Error fetching question:", error);
    } finally {
      setLoading(false);
    }
  };

  const handleAnswer = async (answer) => {
    if (!question || selectedAnswer !== null) return;
    setSelectedAnswer(answer);

    try {
      const response = await axios.post(`${API_URL}/destinations`, {
        action: "validate_destination",
        clue_id: question.clue_id,
        clues: question.clues,
        user_answer: answer,
        user_id: userId,
      });

      const { correct, message, fun_fact, correct_count, wrong_count } = response.data;

      setFeedback(message);
      setFunFact(fun_fact);
      setCorrectCount(correct_count);
      setWrongCount(wrong_count);

      if (correct) {
        setShowConfetti(true);
      } else {
        setShowSadFace(true);
      }
    } catch (error) {
      console.error("Error validating answer:", error);
      setFeedback("⚠️ Error validating answer. Please try again.");
    }
  };

  const challengeFriend = async () => {
    const friendUserId = prompt("Enter your friend's user ID:");
    if (!friendUserId) return;
    try {
      await axios.post(`${API_URL}/users/game-register`, { user_id: friendUserId });
      alert("Friend has been registered for the game!");
      generateInviteLink();
      generateInviteImage();
      setTimeout(() => {
        window.open(`https://wa.me/?text=Join%20me%20in%20this%20Travel%20Quiz!%20Check%20my%20score%3A%20${correctCount}.%20Click%20to%20play:%20${inviteLink}%20&media=${inviteImage}`, '_blank');
      }, 1000);
    } catch (error) {
      console.error("Error registering friend:", error);
      alert("Failed to register friend. Try again.");
    }
  };

  const generateInviteLink = () => {
    if (!userId) return;
    const link = `${window.location.origin}/play?invite=${userId}&score=${correctCount}`;
    setInviteLink(link);
  };

  const generateInviteImage = () => {
    const imageUrl = `${API_URL}/generate-invite-image?user_id=${userId}&score=${correctCount}`;
    setInviteImage(imageUrl);
  };

  return (
    <div className="quiz-container">
      {!isRegistered ? (
        <div>
          <h1>🌍 Travel Quiz</h1>
          <input type="text" placeholder="Enter Name" value={name} onChange={(e) => setName(e.target.value)} />
          <input type="email" placeholder="Enter Email" value={email} onChange={(e) => setEmail(e.target.value)} />
          <input type="password" placeholder="Enter Password" value={password} onChange={(e) => setPassword(e.target.value)} />
          <button onClick={registerUser}>Register & Start Game</button>
        </div>
      ) : (
        <>
          <h1>🌍 Travel Quiz</h1>
          <button className="game-register-btn" onClick={challengeFriend}>📨 Challenge a Friend</button>
          {showConfetti && <Confetti />}
          {loading ? (
            <p>Loading question...</p>
          ) : question ? (
            <>
              <p><strong>Clues:</strong> {question.clues.join(" | ")}</p>
              <div className="options">
                {question.options.map((option) => (
                  <button
                    key={option}
                    className={`option-btn ${selectedAnswer === option ? "selected" : ""}`}
                    onClick={() => handleAnswer(option)}
                    disabled={selectedAnswer !== null}
                  >
                    {option}
                  </button>
                ))}
              </div>
              {feedback && <p className="feedback">{feedback}</p>}
              {showSadFace && <p className="sad-face">😢</p>}
              {funFact && <p className="fun-fact">💡 {funFact}</p>}
              <p>✅ Correct: {correctCount} | ❌ Wrong: {wrongCount}</p>
              <button className="next-btn" onClick={fetchQuestion}>{nextButtonText}</button>
            </>
          ) : (
            <p>Error loading question. Please try again.</p>
          )}
        </>
      )}
    </div>
  );
}

export default App;
