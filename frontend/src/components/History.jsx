import React from "react";
import Typography from "@mui/material/Typography";

import HistoryTable from "./HistoryTable";

const History = () => {
  const [order, setOrder] = React.useState("asc");
  const [history, setHistory] = React.useState([]);
  const [orderBy, setOrderBy] = React.useState("fruitType");
  const [updateData, setUpdateData] = React.useState(false);
  const [hideConsumed, setHideConsumed] = React.useState(false);

  React.useEffect(() => {
    async function getHistoryData() {
      let hideConsumedVariable = "unhide";
      hideConsumed
        ? (hideConsumedVariable = "hide")
        : (hideConsumedVariable = "unhide");
      const response = await fetch(
        `http://localhost:5005/history?filter=${hideConsumedVariable}&page=1&size=10&sort=${orderBy}&order=${order}`,
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
      setUpdateData(false);
    }
    getHistoryData();
  }, [order, orderBy, updateData, hideConsumed]);

  //console.log(history);

  const controlHideConsumed = () => {
    hideConsumed ? setHideConsumed(false) : setHideConsumed(true);
  };

  const consumeProduct = async (imageId) => {
    const response = await fetch(
      `http://localhost:5005/history/consume?imageid=${imageId}`,
      {
        method: "POST",
        headers: { "Content-type": "application/json" },
      }
    );
    //console.log(response);
    if (response.status !== 200) {
      console.log("Error! Invalid Consumption!");
    }
    setUpdateData(true);
  };

  const deleteProduct = async (imageId) => {
    const response = await fetch(
      `http://localhost:5005/history/delete?imageid=${imageId}`,
      {
        method: "DELETE",
        headers: { "Content-type": "application/json" },
      }
    );
    //console.log(response);
    if (response.status !== 200) {
      console.log("Error! Invalid Delete!");
    }
    setUpdateData(true);
  };

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
          deleteProduct={deleteProduct}
          setUpdateData={setUpdateData}
          consumeProduct={consumeProduct}
          controlHideConsumed={controlHideConsumed}
        />
      </div>
    </div>
  );
};

export default History;
