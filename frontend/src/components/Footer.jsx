import React from "react";
import Typography from "@mui/material/Typography";

const Footer = () => {
  return (
    <Typography
      variant="caption"
      display="block"
      gutterBottom
      sx={{
        textAlign: "center",
        height: "2px",
      }}
    >
      Freshness Prediction Engine - COMP3900H11ADigitalHaven 2023 ©
    </Typography>
  );
};

export default Footer;
