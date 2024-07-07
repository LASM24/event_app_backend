// frontend/src/components/EventRegistrations.js
import React, { useEffect, useState } from 'react';
import axios from 'axios';

const EventRegistrations = ({ eventId }) => {
    const [registrations, setRegistrations] = useState([]);

    useEffect(() => {
        const fetchRegistrations = async () => {
            try {
                const token = localStorage.getItem('token');
                const response = await axios.get(`/events/${eventId}/registrations`, {
                    headers: {
                        Authorization: `Bearer ${token}`
                    }
                });
                setRegistrations(response.data);
            } catch (error) {
                alert('Failed to fetch registrations');
            }
        };
        fetchRegistrations();
    }, [eventId]);

    return (
        <div>
            <h2>Registrations</h2>
            <ul>
                {registrations.map(registration => (
                    <li key={registration.id}>
                        User ID: {registration.user_id}
                    </li>
                ))}
            </ul>
        </div>
    );
};

export default EventRegistrations;
