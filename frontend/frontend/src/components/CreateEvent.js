// CreateEvent.js
import React, { useState } from 'react';
import axios from 'axios';

const CreateEvent = () => {
    const [title, setTitle] = useState('');
    const [description, setDescription] = useState('');
    const [date, setDate] = useState('');

    const handleSubmit = async (event) => {
        event.preventDefault();
        try {
            // Puedes usar localStorage para obtener el token si es necesario
            const token = localStorage.getItem('token');

            // Realiza la solicitud POST al backend
            await axios.post('http://localhost:5000/events_create', {
                title,
                description,
                date
            });

            alert('Event created successfully');
            // Puedes redirigir o actualizar la lista de eventos después de crear uno

        } catch (error) {
            console.error('Error creating event:', error);
            alert('Failed to create event');
        }
    };

    return (
        <div>
            <h2>Create Event</h2>
            <form onSubmit={handleSubmit}>
                <div>
                    <label>Title:</label>
                    <input
                        type="text"
                        value={title}
                        onChange={(e) => setTitle(e.target.value)}
                        required
                    />
                </div>
                <div>
                    <label>Description:</label>
                    <textarea
                        value={description}
                        onChange={(e) => setDescription(e.target.value)}
                        required
                    />
                </div>
                <div>
                    <label>Date:</label>
                    <input
                        type="datetime-local"
                        value={date}
                        onChange={(e) => setDate(e.target.value)}
                        required
                    />
                </div>
                <button type="submit">Create Event</button>
            </form>
        </div>
    );
};

export default CreateEvent;
