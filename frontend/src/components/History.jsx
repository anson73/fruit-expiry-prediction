import React from "react";
import Typography from "@mui/material/Typography";

import HistoryTable from "./HistoryTable";

const History = () => {
  return (
    <div
      className="historyPage"
      style={{
        paddingTop: "5%",
        //border: "1px solid red",
        //display: "flex",
        justifyContent: "center",
        alignItems: "center",
        overflow: "",
      }}
    >
      <Typography
        variant="caption"
        display="block"
        gutterBottom
        sx={{
          textAlign: "center",
          //display: "flex",
          //alignItems: "Center",
          //justifyContent: "Center",
        }}
      >
        <h1>Welcome back! This is your freshness prediction history!</h1>
      </Typography>
      <div
        style={{
          //border: "10px solid red",
          display: "flex",
          justifyContent: "center",
          alignItems: "center",
        }}
      >
        <HistoryTable />
      </div>
    </div>
  );
};

export default History;
