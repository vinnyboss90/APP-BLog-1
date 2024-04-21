import React, { useState, useEffect } from 'react';
import axios from 'axios';

const Profile = () => {
  const [username, setUsername] = useState('');
  const [image, setImage] = useState('');
  const [blogs, setBlogs] = useState([]);
  const [savedUsers, setSavedUsers] = useState([]);
  const [currentUserId, setCurrentUserId] = useState(null);

  useEffect(() => {
    // Fetch blogs from the backend
    axios.get('/api/blogs')
      .then(response => {
        setBlogs(response.data);
      })
      .catch(error => {
        console.error('Error fetching blogs:', error);
      });

    // Fetch saved users from the backend
    axios.get('/api/users')
      .then(response => {
        setSavedUsers(response.data);
      })
      .catch(error => {
        console.error('Error fetching saved users:', error);
      });
  }, []);

  const handleSaveProfile = () => {
    // Check if username already exists
    if (savedUsers.some(user => user.username === username)) {
      alert('Username already exists. Please choose a different one.');
      return;
    }

    // Save profile
    axios.post('/api/profile', { username, image })
      .then(response => {
        console.log('Profile saved successfully:', response.data);
        setCurrentUserId(response.data.id);
        // Add the saved user to the list of saved users
        setSavedUsers([...savedUsers, response.data]);
      })
      .catch(error => {
        console.error('Error saving profile:', error);
      });
  };

  const handleUsernameChange = (e) => {
    setUsername(e.target.value);
  };

  const handleImageChange = (e) => {
    // Handle image upload
    setImage(e.target.files[0]);
  };

  const handlePostBlog = (content) => {
    // Post a new blog
    axios.post('/api/blogs', { userId: currentUserId, content })
      .then(response => {
        console.log('Blog posted successfully:', response.data);
        // Update the list of blogs
        setBlogs([...blogs, response.data]);
      })
      .catch(error => {
        console.error('Error posting blog:', error);
      });
  };

  return (
    <div className="container mx-auto my-8">
      {currentUserId ? (
        <div className="flex flex-wrap justify-center">
          <div className="w-64 m-4">
            <img src={image} alt={username} className="w-full mb-2 rounded" />
            <p className="text-center">{username}</p>
          </div>
          <div className="w-full my-4">
            <textarea
              placeholder="Write your blog here..."
              className="w-full p-2 border border-gray-300 rounded"
              rows="4"
              onChange={(e) => handlePostBlog(e.target.value)}
            />
          </div>
        </div>
      ) : (
        <div className="flex flex-wrap justify-center">
          <div className="w-64 m-4">
            <input
              type="text"
              placeholder="Enter username"
              value={username}
              onChange={handleUsernameChange}
              className="w-full mb-2 p-2 border border-gray-300 rounded"
            />
            <input
              type="file"
              onChange={handleImageChange}
              className="w-full mb-4"
            />
            <button onClick={handleSaveProfile} className="bg-blue-500 text-white py-2 px-4 rounded">
              Save Profile
            </button>
          </div>
        </div>
      )}
      <div className="w-full my-8">
        <h2 className="text-2xl font-bold mb-4">Blogs</h2>
        {blogs.map(blog => (
          <div key={blog.id} className="border border-gray-300 p-4 rounded mb-4">
            <p>{blog.content}</p>
          </div>
        ))}
      </div>
    </div>
  );
};

export default Profile;
