// frontend/src/components/RegisterEvent.js
import React, { useState } from 'react';
import axios from 'axios';

const RegisterEvent = ({ eventId }) => {
    const handleRegister = async () => {
        try {
            const token = localStorage.getItem('token');
            await axios.post(`/events/${eventId}/register`, {}, {
                headers: {
                    Authorization: `Bearer ${token}`
                }
            });
            alert('Registered for event successfully');
        } catch (error) {
            alert('Event registration failed');
        }
    };

    return (
        <button onClick={handleRegister}>Register for Event</button>
    );
};

export default RegisterEvent;
