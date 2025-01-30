import React, { useEffect, useState } from 'react';
import axios from 'axios';

function Onboarding() {
  const [userData, setUserData] = useState({
    firstName: '',
    lastName: '',
    phone: '',
    registrationNo: '',
    email: ''
  });

  useEffect(() => {
    const userEmail = localStorage.getItem('userEmail');

    if (!userEmail) {
      alert('You must be logged in to view this page.');
      return;
    }

    axios.get(`http://127.0.0.1:5000/onboarding`, { params: { email: userEmail } })
      .then((res) => {
        setUserData({
          firstName: res.data.first_name,
          lastName: res.data.last_name,
          phone: res.data.phone,
          registrationNo: res.data.registration_no,
          email: res.data.email
        });
      })
      .catch((err) => alert('Error fetching user data: ' + (err.response?.data?.message || err.message)));
  }, []);

  const handleChange = (e) => {
    setUserData({ ...userData, [e.target.name]: e.target.value });
  };

  const handleUpdate = async () => {
    try {
      const userEmail = localStorage.getItem('userEmail');
      if (!userEmail) {
        alert('You must be logged in to update details.');
        return;
      }

      await axios.put('http://127.0.0.1:5000/onboarding', { ...userData, email: userEmail });
      alert('User details updated!');
    } catch (err) {
      alert('Error updating details: ' + (err.response?.data?.message || err.message));
    }
  };

  return (
    <div>
      <h1>Onboarding</h1>
      <form>
        <label>
          First Name:
          <input
            type="text"
            name="firstName"
            value={userData.firstName}
            onChange={handleChange}
          />
        </label>
        <label>
          Last Name:
          <input
            type="text"
            name="lastName"
            value={userData.lastName}
            onChange={handleChange}
          />
        </label>
        <label>
          Mobile No.:
          <input
            type="text"
            name="phone"
            value={userData.phone}
            onChange={handleChange}
          />
        </label>
        <label>
          Email:
          <input
            type="text"
            name="email"
            value={userData.email}
            readOnly
          />
        </label>
        <label>
          College Registration No.:
          <input
            type="text"
            name="registrationNo"
            value={userData.registrationNo}
            readOnly
          />
        </label>
        <button type="button" onClick={handleUpdate}>Update Details</button>
      </form>
    </div>
  );
}

export default Onboarding;
