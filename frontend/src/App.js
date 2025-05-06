import React, { useState, useEffect } from 'react';
import API from './api';
import './App.css';

function App() {
  const [auth, setAuth] = useState(false);
  const [loginForm, setLoginForm] = useState({ username: '', password: '' });
  const [form, setForm] = useState({ title: '', content: '' });
  const [notes, setNotes] = useState([]);
  const [message, setMessage] = useState('');

  // Login
  const handleLogin = async (e) => {
    e.preventDefault();
    try {
      const form = new URLSearchParams();
      form.append("username", loginForm.username);
      form.append("password", loginForm.password);
  
      const res = await API.post('/token', form, {
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded'
        }
      });
  
      localStorage.setItem("token", res.data.access_token);
      setAuth(true);
      setLoginForm({ username: '', password: '' });
      fetchNotes();
    } catch (err) {
      alert('Login failed. Please check your username/password.');
      console.error(err);
    }
  };
  

  // Logout
  const handleLogout = () => {
    localStorage.removeItem('token');
    setAuth(false);
    setNotes([]);
    setForm({ title: '', content: '' });
  };

  // Fetch notes from backend
  const fetchNotes = async () => {
    try {
      const res = await API.get('/notes');
      setNotes(res.data);
    } catch (err) {
      console.error('Error fetching notes:', err);
    }
  };

  // Add a new note
  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const res = await API.post('/notes', form);
      setMessage('Note saved!');
      setForm({ title: '', content: '' });
      fetchNotes();
    } catch (err) {
      setMessage('Error saving note.');
    }
  };

  // Analyze sentiment
  const handleAnalyze = async (id) => {
    try {
      const res = await API.get(`/notes/${id}/analyze`);
      const updatedNotes = notes.map(n =>
        n.id === id ? { ...n, sentiment: res.data.sentiment } : n
      );
      setNotes(updatedNotes);
    } catch (err) {
      console.error('Analysis failed');
    }
  };

  // Load token on page load
  useEffect(() => {
    if (localStorage.getItem('token')) {
      setAuth(true);
      fetchNotes();
    }
  }, []);

  return (
    <div className="container">
      <h1>AI Notes App</h1>

      {!auth ? (
        <form onSubmit={handleLogin}>
          <input
            type="text"
            placeholder="Username"
            value={loginForm.username}
            onChange={(e) => setLoginForm({ ...loginForm, username: e.target.value })}
            required
          />
          <input
            type="password"
            placeholder="Password"
            value={loginForm.password}
            onChange={(e) => setLoginForm({ ...loginForm, password: e.target.value })}
            required
          />
          <button type="submit">Login</button>
        </form>
      ) : (
        <>
          <button onClick={handleLogout}>Logout</button>

          <form onSubmit={handleSubmit}>
            <input
              type="text"
              placeholder="Title"
              value={form.title}
              onChange={(e) => setForm({ ...form, title: e.target.value })}
              required
            />
            <textarea
              placeholder="Content (10+ chars)"
              rows="4"
              value={form.content}
              onChange={(e) => setForm({ ...form, content: e.target.value })}
              required
            />
            <button type="submit">Save Note</button>
            <p>{message}</p>
          </form>

          <h2>All Notes</h2>
          {notes.map(note => (
            <div className="note" key={note.id}>
              <h3>{note.title}</h3>
              <p>{note.content}</p>
              <p className="sentiment">
                Sentiment: {note.sentiment || 'Not analyzed'}
              </p>
              <button onClick={() => handleAnalyze(note.id)}>
                Analyze
              </button>
            </div>
          ))}
        </>
      )}
    </div>
  );
}

export default App;
