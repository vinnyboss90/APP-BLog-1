import React from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import HomePage from './component/Header';
import AboutPage from './component/AboutPage';
import Footer from './component/footer';
import { Login } from './component/Login';
import { SignUp } from './component/SignUp';
import { DevelopersPage } from './component/DevelopersPage';
import { Home } from './component/Home';
import BlogPage from './component/BlogPage';

function App() {
  return (
    <BrowserRouter>
      <div className="container mx-auto px-4">
      <HomePage />
      </div>

      <div className="container mx-auto px-4 sm:px-6 lg:px-8">
        <Routes>
          <Route exact path="/" element={<Home/>} />
          <Route exact path="/about" element={<AboutPage />} />
          <Route exact path="/blog" element={<BlogPage />} />
          <Route exact path="/developer" element={<DevelopersPage />} />
          <Route exact path="/login" element={<Login />} />
          <Route exact path="/signup" element={<SignUp />} />


        </Routes>
      </div>

      <div className=''>
      <Footer/>
      </div>
      
     
    </BrowserRouter>
  );
}

export default App;
