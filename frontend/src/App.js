import React, { useState, useEffect } from 'react';
import axios from 'axios';

const API_BASE = "http://localhost:8000";
const API_KEY = "mysecretkey";

function App() {
  const [notes, setNotes] = useState([]);
  const [form, setForm] = useState({ title: '', content: '' });
  const [message, setMessage] = useState('');

  // Load all notes
  const fetchNotes = async () => {
    try {
      const res = await axios.get(`${API_BASE}/notes`, {
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
      const res = await axios.post(`${API_BASE}/notes`, form, {
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
      const res = await axios.get(`${API_BASE}/notes/${id}/analyze`, {
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
    <div style={{ padding: '2rem', maxWidth: '600px', margin: '0 auto' }}>
      <h1>📝 AI Notes App</h1>

      <form onSubmit={handleSubmit}>
        <input
          type="text"
          placeholder="Title"
          value={form.title}
          onChange={(e) => setForm({ ...form, title: e.target.value })}
          required
        /><br /><br />
        <textarea
          placeholder="Content (10+ chars)"
          rows="4"
          value={form.content}
          onChange={(e) => setForm({ ...form, content: e.target.value })}
          required
        /><br /><br />
        <button type="submit">Save Note</button>
        <p>{message}</p>
      </form>

      <h2>All Notes</h2>
      {notes.map(note => (
        <div key={note.id} style={{ border: '1px solid #ccc', padding: '1rem', marginBottom: '1rem' }}>
          <h3>{note.title}</h3>
          <p>{note.content}</p>
          <p>
            Sentiment: {note.sentiment || 'Not analyzed'}
            <button onClick={() => handleAnalyze(note.id)} style={{ marginLeft: '1rem' }}>
              Analyze
            </button>
          </p>
        </div>
      ))}
    </div>
  );
}

export default App;
