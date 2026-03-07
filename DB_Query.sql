select * from user_answers;
select * from questions;
select * from users;
show columns
SELECT q.category,
       COUNT(a.id) AS total,
       SUM(CASE WHEN a.is_weak = true THEN 1 ELSE 0 END) AS weak
FROM user_answers a
JOIN questions q ON q.id = a.question_id
WHERE a.user_id = 'your_user_id'
GROUP BY q.category;
INSERT INTO questions (id, question_text, category, difficulty, source)
VALUES
(gen_random_uuid()::text, 'What is the difference between a list and a tuple in Python? When would you use each?', 'Python', 'Medium', 'Manual'),
(gen_random_uuid()::text, 'Explain the difference between deep copy and shallow copy in Python.', 'Python', 'Medium', 'Manual'),

(gen_random_uuid()::text, 'What is the difference between INNER JOIN, LEFT JOIN, RIGHT JOIN, and FULL JOIN?', 'SQL', 'Medium', 'Manual'),
(gen_random_uuid()::text, 'How do you find the second highest salary in SQL?', 'SQL', 'Hard', 'Manual'),

(gen_random_uuid()::text, 'What are the steps you follow when performing exploratory data analysis (EDA)?', 'Data Analysis', 'Medium', 'Manual'),
(gen_random_uuid()::text, 'How do you handle missing values in a dataset?', 'Data Analysis', 'Medium', 'Manual'),

(gen_random_uuid()::text, 'What is the difference between supervised and unsupervised learning?', 'Machine Learning', 'Medium', 'Manual'),
(gen_random_uuid()::text, 'Explain bias vs variance tradeoff in machine learning.', 'Machine Learning', 'Hard', 'Manual'),

(gen_random_uuid()::text, 'What is ETL and how is it different from ELT?', 'ETL', 'Medium', 'Manual'),
(gen_random_uuid()::text, 'What challenges have you faced while building data pipelines?', 'ETL', 'Medium', 'Manual'),

(gen_random_uuid()::text, 'Tell me about yourself.', 'HR', 'Easy', 'Manual'),
(gen_random_uuid()::text, 'Describe a challenging project you worked on and how you handled it.', 'HR', 'Medium', 'Manual'),

(gen_random_uuid()::text, 'What is the difference between a calculated field and a parameter in Tableau?', 'Dashboard', 'Medium', 'Manual'),
(gen_random_uuid()::text, 'How do you design an effective dashboard?', 'Dashboard', 'Medium', 'Manual'),

(gen_random_uuid()::text, 'What is overfitting and how do you prevent it?', 'Data Science', 'Medium', 'Manual'),
(gen_random_uuid()::text, 'Explain cross-validation and why it is important.', 'Data Science', 'Medium', 'Manual'),

(gen_random_uuid()::text, 'What is the difference between loc and iloc in pandas?', 'Python', 'Medium', 'Manual'),
(gen_random_uuid()::text, 'How do you optimize a slow pandas operation?', 'Python', 'Hard', 'Manual'),

(gen_random_uuid()::text, 'How would you analyze why sales dropped by 15% last month?', 'Data Analysis', 'Hard', 'Manual'),
(gen_random_uuid()::text, 'If a dashboard KPI suddenly spikes abnormally, how would you investigate?', 'Dashboard', 'Hard', 'Manual');
-- SELECT questions WHERE category='SQL' AND difficulty='Medium'
SELECT DISTINCT category FROM questions;

UPDATE questions SET category = 'General'
WHERE category IS NULL;
