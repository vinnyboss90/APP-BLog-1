import React, { useState, useEffect } from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';

import HomePage from './component/HomePage';
import AboutPage from './component/AboutPage';
import Home from './component/Home';
import DevelopersPage from './component/DevelopersPage';
import BlogsPage from './component/Home';
import ArticleList from './component/ArticleList';
import Form from './component/Form';

function App() {
  const [articles, setArticles] = useState([]);
  const [editedArticle, setEditedArticle] = useState(null);

  useEffect(() => {
    fetch('http://127.0.0.1:5000/get', {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json'
      }
    })
      .then(res => res.json())
      .then(data => {
        console.log(data);
        setArticles(data);
      })
      .catch(error => {
        console.error('Error:', error);
      });
  }, []);

  const editArticle = (article) => {
    setEditedArticle(article);
  };

  const updatedData = (article) => {
    const new_article = articles.map(my_article => {
      if (my_article.id === article.id) {
        return article;
      } else {
        return my_article;
      }
    });
    setArticles(new_article);
  };

  const openForm = () => {
    setEditedArticle({
      title: "",
      body: ""
    });
  };

  const insertedArticle = (article) => {
    const new_articles = [...articles, article];
    setArticles(new_articles);
  };

  const deleteArticle = (article) => {
    const new_articles = articles.filter(myarticle => {
      if (myarticle.id === article.id) {
        return false;
      }
      return true;
    });
    setArticles(new_articles);
  };

  return (
    <BrowserRouter>
      <div className="container mx-auto px-4">
        <div className="p-4">
          <h1 className="text-2xl font-bold text-center">All Pulse Blog</h1>
        </div>
        <div>
          <button className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded mt-4" onClick={openForm}>Post Blog</button>
        </div>
      </div>

      <div className="container mx-auto px-4 sm:px-6 lg:px-8">
        <Routes>
          <Route exact path="/" element={<Home />} />
          <Route exact path="/about" element={<AboutPage />} />
          <Route exact path="/blogs" element={<BlogsPage />} />
          <Route exact path="/developer" element={<DevelopersPage />} />
        </Routes>
        <HomePage />
      </div>

      <ArticleList articles={articles} editArticle={editArticle} deleteArticle={deleteArticle} />
      {editedArticle ? <Form article={editedArticle} updatedData={updatedData} insertedArticle={insertedArticle} /> : null}
    </BrowserRouter>
  );
}

export default App;
