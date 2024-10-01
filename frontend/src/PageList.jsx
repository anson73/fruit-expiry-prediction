import React from "react";
import { Routes, Route, useNavigate } from "react-router-dom";

import Box from "@mui/material/Box";
import BottomNavigation from "@mui/material/BottomNavigation";
import BottomNavigationAction from "@mui/material/BottomNavigationAction";
import RestoreIcon from "@mui/icons-material/Restore";

import Footer from "./components/Footer";
import Login from "./components/Login";
import Register from "./components/Register";

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
    const response = await fetch("http://localhost:5005/user/auth/logout", {
      method: "POST",
      body: JSON.stringify({}),
      headers: {
        "Content-type": "application/json",
        Authorization: `Bearer ${token}`,
      },
    });
    const data = await response.json();
    if (data.error) {
      alert(data.error);
    } else {
      setToken(null);
      localStorage.removeItem("token");
      localStorage.removeItem("email");
      navigate("/listings");
      // console.log('logged out');
    }
  };

  const pages = token
    ? ["Prediction", "History", "Logout"]
    : ["Register", "Login"];

  return (
    <>
      <Routes>
        <Route path="/" element={<Login />} />
        <Route
          path="/register"
          element={<Register token={token} setToken={setToken} />}
        />
        <Route
          path="/login"
          element={<Login token={token} setToken={setToken} />}
        />
      </Routes>
      <Box
        style={{
          height: "15vh",
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
