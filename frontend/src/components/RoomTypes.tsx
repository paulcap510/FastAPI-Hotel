import React, { useEffect, useState } from 'react';

interface RoomType {
  id: number;
  name: string;
  description: string;
  price_per_night: number;
}

const RoomTypes: React.FC = () => {
  const [roomTypes, setRoomTypes] = useState<RoomType[]>([]);
  const [loading, setLoading] = useState<boolean>(true);

  useEffect(() => {
    const fetchRoomTypes = async () => {
      try {
        const response = await fetch('http://127.0.0.1:8000/rooms/room-types/');
        const data = await response.json();
        setRoomTypes(data);
        setLoading(false);
      } catch (error) {
        console.error('Error fetching room types:', error);
        setLoading(false);
      }
    };

    fetchRoomTypes();
  }, []);

  if (loading) {
    return <div>Loading...</div>;
  }

  return (
    <div className="room-types">
      <h1>Room Types</h1>
      <ul>
        {roomTypes.map((roomType) => (
          <li key={roomType.id}>
            <h2>{roomType.name}</h2>
            <p>{roomType.description}</p>
            <p>Price per night: ${roomType.price_per_night}</p>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default RoomTypes;
