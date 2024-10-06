import React from "react";
import { Routes, Route, useNavigate } from "react-router-dom";

import Box from "@mui/material/Box";
import BottomNavigation from "@mui/material/BottomNavigation";
import BottomNavigationAction from "@mui/material/BottomNavigationAction";
import RestoreIcon from "@mui/icons-material/Restore";

import Footer from "./components/Footer";
import Login from "./components/Login";
import Register from "./components/Register";
import History from "./components/History";
import Prediction from "./components/Prediction";
import Profile from "./components/Profile";
import Landpage from "./components/Landpage";

const PageList = () => {
  const [token, setToken] = React.useState(null);
  const [email, setEmail] = React.useState("");
  const navigate = useNavigate();

  React.useEffect(() => {
    const checktoken = localStorage.getItem("token");
    if (checktoken) {
      setToken(checktoken);
      setEmail(localStorage.getItem("email"));
    }
  }, []);

  const logout = async () => {
    //const response = await fetch("http://localhost:5005/user/auth/logout", {
    //  method: "POST",
    //  body: JSON.stringify({}),
    //  headers: {
    //    "Content-type": "application/json",
    //    Authorization: `Bearer ${token}`,
    //  },
    //});
    //const data = await response.json();
    //if (data.error) {
    //  alert(data.error);
    //} else {
    //  setToken(null);
    //  localStorage.removeItem("token");
    //  localStorage.removeItem("email");
    //  navigate("/listings");
    //  // console.log('logged out');
    //}
    setToken(null);
    localStorage.removeItem("token");
    navigate("/login");
  };

  const pages = token
    ? ["Prediction", "History", "Profile", "Logout"]
    : ["Register", "Login"];

  return (
    <>
      <Box
        style={{
          height: "calc(100vh - 118px)",
          //border: "1px solid red",
          overflow: "auto",
        }}
      >
        <Routes>
          <Route path="/" element={<Landpage />} />
          <Route path="/history" element={<History />} />
          <Route path="/prediction" element={<Prediction />} />
          <Route path="/profile" element={<Profile />} />
          <Route path="/landpage" element={<Landpage />} />
          <Route
            path="/register"
            element={<Register token={token} setToken={setToken} />}
          />
          <Route
            path="/login"
            element={<Login token={token} setToken={setToken} />}
          />
        </Routes>
      </Box>
      <Box
        style={{
          height: "110px",
          // border: '1px solid red',
        }}
      >
        <hr />
        <Box>
          <BottomNavigation
            showLabels
            value={""}
            onChange={(event, newValue) => {
              if (pages[newValue] === "Logout") {
                logout();
              } else {
                navigate(`/${pages[newValue].toLowerCase()}`);
              }
            }}
          >
            {pages.map((page, idx) => {
              return (
                <BottomNavigationAction
                  label={page}
                  id={page}
                  icon={<RestoreIcon />}
                  key={idx}
                />
              );
            })}
          </BottomNavigation>
        </Box>
        <hr />
        <Footer />
      </Box>
    </>
  );
};

export default PageList;

/*
 âœ… useState -- easy
 âœ… useEffect
 âœ… multiple files, components
 âœ… props
 âœ… routing & spas
 âœ… css framewrosk
 âœ… (refersher) fetch
*/
