const mysql = require('mysql2/promise');
const env = require('dotenv').config({ path: "../../.env" });

const db = async () => {
    try {
        let connection = await mysql.createConnection({
            host: process.env.host,
            user: process.env.user,
            port: process.env.port,
            password: process.env.password,
            database: process.env.database
        });

        let [rows, fields] = await connection.query('SELECT * FROM st_info');
        console.log(rows);

        let data = {
            st_id: "202599",
            name: "Moon",
            dept: "computer"
        };

        let insertId = data.st_id;

        [rows, fields] = await connection.query(
            "INSERT INTO st_info (st_id, name, dept) VALUES (?, ?, ?)", 
            [data.st_id, data.name, data.dept]
        );
        console.log("\nData is inserted~!!");

        // Select * query for inserted data
        [rows, fields] = await connection.query("SELECT * FROM st_info WHERE st_id = ?", [insertId]);
        console.log(rows);

        // Update query
        [rows, fields] = await connection.query(
            "UPDATE st_info SET dept = ? WHERE st_id = ?",
            ["Game", insertId]
        );
        console.log("\nData is Updated~!!");

        // Select * query for updated data
        [rows, fields] = await connection.query("SELECT * FROM st_info WHERE st_id = ?", [insertId]);
        console.log(rows);

        // Delete query
        [rows, fields] = await connection.query("DELETE FROM st_info WHERE st_id = ?", [insertId]);
        console.log("\nData is Deleted~!!");

        // Select * query for deleted data
        [rows, fields] = await connection.query("SELECT * FROM st_info");
        console.log(rows);
        
        await connection.end();  

    } catch (error) {
        console.log(error);
    }
};

db();

