import React, { useState } from 'react';
import axios from 'axios';
import './App.css';

function App() {
  const [userInput, setUserInput] = useState('');
  const [feedback, setFeedback] = useState('');
  const [continuation, setContinuation] = useState('');

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

  return (
    <div className='App'>
      <header className='header'>
        <h1>Creative Writing Therapy</h1>
      </header>
      <section className='form-section'>
        <form onSubmit={handleSubmit} className='form'>
          <textarea 
            className='textarea' 
            value={userInput} 
            onChange={(e) => setUserInput(e.target.value)} 
            placeholder='Enter your story here...' 
            rows="8" 
            cols="50" 
          />
          <button className='submit-button' type="submit">Submit</button>
        </form>
      </section>
      <section className='results-section'>
        <h2>Feedback:</h2>
        <p>{feedback}</p>
        <h2>Generated Continuation:</h2>
        <p>{continuation}</p>
      </section>
    </div>
  );
}

export default App;
