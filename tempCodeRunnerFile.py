    FROM users
    INNER JOIN quens ON users.question_id = quens.qid
    WHERE users.username = %s'''