import React, { useState } from 'react';
import axios from 'axios';
import './App.css';

function App() {
  const [userInput, setUserInput] = useState('');
  const [feedback, setFeedback] = useState('');
  const [continuation, setContinuation] = useState('');
  const [submitted, setSubmit] = useState(false);
  // Poetry
  const [poemLines, setPoemLines] = useState([]);
  const [currentTurn, setCurrentTurn] = useState('user');
  const [poemInput, setPoemInput] = useState('');
  const [poemInstructions, setPoemInstructions] = useState("You start the poem!");

  const handleSubmit = async (event) => {
    event.preventDefault();
    try {
      const response = await axios.post('http://127.0.0.1:8000/api/', { user_input: userInput }, {
        headers: {
          'Content-Type': 'application/json',
        }
      });
      setFeedback(response.data.feedback);
      setContinuation(response.data.continuation);
    } catch (err) {
      console.error("Error making request", err);
    }
  }

  const handlePoemSubmit = async (event) => {
    event.preventDefault();
    setSubmit(true);
    if (currentTurn === 'user') {
      setPoemLines([...poemLines, `User: ${poemInput}`]);
      setPoemInput('');
      setCurrentTurn('ai')
      setPoemInstructions('AI is thinking, one moment...');
      try {
        const response = await axios.post('http://127.0.0.1:8000/api/poem/', { line: poemInput }, {
          headers: {
            'Content-Type': 'application/json',
          }
        });
        setPoemLines([...poemLines, `User: ${poemInput}`, `AI: ${response.data.ai_line}`]);
        setPoemInput('');
        setCurrentTurn('user');
        setPoemInstructions("It's your turn again! Add the next line.");
      } catch (err) {
        console.error("Error making request", err);
      }
    }
  }

  return (
    <div className='App'>
      <header className='header'>
        <h1>Creative Writing Therapy</h1>
      </header>
      <section className='form-section'>
        <h2>Creative Writing</h2>
        <form onSubmit={handleSubmit} className='form'>
          <textarea 
            className='textarea' 
            value={userInput} 
            onChange={(e) => setUserInput(e.target.value)} 
            placeholder='Enter your story here...' 
            rows="8" 
            cols="50" 
          />
          <button 
            className='submit-button' 
            type="submit"
          >
            {submitted ? "Loading..." : "Submit"} 
          </button>
        </form>
        <div className='results-section'>
          <h3>Feedback:</h3>
          <p>{feedback}</p>
          <h3>Generated Continuation:</h3>
          <p>{continuation}</p>
        </div>
      </section>

      <section className='poem-section'>
        <h2>Create a Poem</h2>
        <p>{poemInstructions}</p>
        <form onSubmit={handlePoemSubmit} className='poem-form'>
          <textarea 
            className='textarea' 
            value={poemInput} 
            onChange={(e) => setPoemInput(e.target.value)} 
            placeholder={currentTurn === 'user' ? 'Your turn to add a line...' : 'AI is generating a line...'} 
            rows="5" 
            cols="50" 
            readOnly={currentTurn === 'ai'} 
          />
          <button className='submit-button' type="submit">{currentTurn === 'user' ? 'Add Line' : 'Waiting...'}</button>
        </form>
        <div className='poem-lines'>
          {poemLines.map((line, index) => (
            <p key={index}>{line}</p>
          ))}
        </div>
      </section>
    </div>
  );
}

export default App;
