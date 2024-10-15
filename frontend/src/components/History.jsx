import React from "react";
import Typography from "@mui/material/Typography";

import HistoryTable from "./HistoryTable";

const History = () => {
  const [order, setOrder] = React.useState("asc");
  const [history, setHistory] = React.useState([]);
  const [orderBy, setOrderBy] = React.useState("fruitType");

  React.useEffect(() => {
    async function getHistoryData() {
      const response = await fetch(
        `http://localhost:5005/history?filter=unhide&page=1&size=10&sort=${orderBy}&order=${order}`,
        {
          method: "GET",
          headers: {
            "Content-type": "application/json",
          },
        }
      );
      const data = await response.json();
      setHistory(data);
      console.log(data);
    }
    getHistoryData();
  }, [order, orderBy]);

  console.log(history);

  return (
    <div
      className="historyPage"
      style={{
        paddingTop: "3rem",
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
        <h1>Welcome! This is your freshness prediction history!</h1>
      </Typography>
      <div
        style={{
          //border: "10px solid red",
          display: "flex",
          justifyContent: "center",
          alignItems: "center",
        }}
      >
        <HistoryTable
          historyData={history}
          order={order}
          orderBy={orderBy}
          setOrder={setOrder}
          setOrderBy={setOrderBy}
        />
      </div>
    </div>
  );
};

export default History;
