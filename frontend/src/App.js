import './App.css';
import React, { useState, useEffect } from 'react';
import API from './api';

const API_BASE = "http://localhost:8000";
const API_KEY = "mysecretkey";

function App() {
  const [notes, setNotes] = useState([]);
  const [form, setForm] = useState({ title: '', content: '' });
  const [message, setMessage] = useState('');

  // Load all notes
  const fetchNotes = async () => {
    try {
      const res = await API.get(`${API_BASE}/notes`, {
        headers: { "x-api-key": API_KEY }
      });
      setNotes(res.data);
    } catch (err) {
      console.error(err);
    }
  };

  // Submit new note
  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const res = await API.post(`${API_BASE}/notes`, form, {
        headers: { "x-api-key": API_KEY }
      });
      setMessage("Note saved!");
      setForm({ title: '', content: '' });
      fetchNotes();
    } catch (err) {
      setMessage("Error saving note.");
    }
  };

  // Analyze sentiment
  const handleAnalyze = async (id) => {
    try {
      const res = await API.get(`${API_BASE}/notes/${id}/analyze`, {
        headers: { "x-api-key": API_KEY }
      });
      const updatedNotes = notes.map(n => (
        n.id === id ? { ...n, sentiment: res.data.sentiment } : n
      ));
      setNotes(updatedNotes);
    } catch (err) {
      console.error(err);
    }
  };

  useEffect(() => {
    fetchNotes();
  }, []);

  return (
    <div className="container">
      <h1>AI Notes App</h1>
  
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
    </div>
  );
  
}

export default App;
