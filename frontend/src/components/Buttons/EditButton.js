import React, { useState } from "react";
import { Redirect, Router } from "react-router-dom";

const EditButton = React.memo (({ data, type }) => {
    let [page, setPage] = useState('');

    if (page === "edit") {
        window.location.href = `/edit?description=${data}&type=${type}`;
    }

    return (
        <div className="icon-container"
             onClick={() => setPage("edit")}>
            <img className="icon" src="./edit.svg" alt="edit"/>
        </div>
    );
}, (prev, cur) => prev === cur ? false : true)

export default EditButton;