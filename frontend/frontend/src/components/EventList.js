// frontend/src/components/EventList.js
import React, { useEffect, useState } from 'react';
import axios from 'axios';

const EventList = () => {
    const [events, setEvents] = useState([]);

    useEffect(() => {
        const fetchEvents = async () => {
            const response = await axios.get('/events');
            setEvents(response.data);
        };
        fetchEvents();
    }, []);

    return (
        <div>
            <h2>Events</h2>
            <ul>
                {events.map(event => (
                    <li key={event.id}>
                        <h3>{event.title}</h3>
                        <p>{event.description}</p>
                        <p>{new Date(event.date).toLocaleString()}</p>
                    </li>
                ))}
            </ul>
        </div>
    );
};

export default EventList;
