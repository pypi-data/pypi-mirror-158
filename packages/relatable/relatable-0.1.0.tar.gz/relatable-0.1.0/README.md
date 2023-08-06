# relatable

relatable is a Python package for converting a collection of documents, 
such as a MongoDB collection, into an interrelated set of tables, such as a 
schema in a relational database.

## Instalation

```
pip3 install relatable
```

## Example of use

Consider the following list of dictionaries:

```
docs = [
  {
    "name": "Alice",
    "age": 34,
    "experience": [
      {
        "company": "Google",
        "role": "Software Engineer",
        "from": 2020,
        "to": 2022,
        "responsibilities": [
          "Google stuff",
          "Mark TensorFlow issues as \"Won't Do\""
        ]
      },
      {
        "company": "Facebook",
        "role": "Senior Data Scientist",
        "from": 2017,
        "to": 2020,
        "responsibilities": [
          "Censor media",
          "Learn the foundations of ML",
          "Do Kaggle competitions"
        ]
      }
    ]
  },
  {
    "name": "Bob",
    "age": 27,
    "experience": [
      {
        "company": "OpenAI",
        "role": "NLP Engineer",
        "from": 2019,
        "to": 2022,
        "responsibilities": [
          "Assert that GPT-2 is racist",
          "Assert that GPT-3 is racist",
          "Develop a prototype of a premium non-racist language model"
        ]
      }
    ]
  }
]
```

To convert `docs` into a set of tables:

```
from relatable import make_relational_schema

tables = make_relational_schema(docs)
```

The result is the following:

```
[
  [
    {
      "[id_0]": 0,
      "name": "Alice",
      "age": 34
    },
    {
      "[id_0]": 1,
      "name": "Bob",
      "age": 27
    }
  ],
  [
    {
      "[id_1]": 0,
      "[id_0]": 0,
      "experience.company": "Google",
      "experience.role": "Software Engineer",
      "experience.from": 2020,
      "experience.to": 2022
    },
    {
      "[id_1]": 1,
      "[id_0]": 0,
      "experience.company": "Facebook",
      "experience.role": "Senior Data Scientist",
      "experience.from": 2017,
      "experience.to": 2020
    },
    {
      "[id_1]": 2,
      "[id_0]": 1,
      "experience.company": "OpenAI",
      "experience.role": "NLP Engineer",
      "experience.from": 2019,
      "experience.to": 2022
    }
  ],
  [
    {
      "[id_2]": 0,
      "[id_1]": 0,
      "[id_0]": 0,
      "experience.responsibilities": "Google stuff"
    },
    {
      "[id_2]": 1,
      "[id_1]": 0,
      "[id_0]": 0,
      "experience.responsibilities": "Mark TensorFlow issues as \"Won't Do\""
    },
    {
      "[id_2]": 2,
      "[id_1]": 1,
      "[id_0]": 0,
      "experience.responsibilities": "Censor media"
    },
    {
      "[id_2]": 3,
      "[id_1]": 1,
      "[id_0]": 0,
      "experience.responsibilities": "Learn the foundations of ML"
    },
    {
      "[id_2]": 4,
      "[id_1]": 1,
      "[id_0]": 0,
      "experience.responsibilities": "Do Kaggle competitions"
    },
    {
      "[id_2]": 5,
      "[id_1]": 2,
      "[id_0]": 1,
      "experience.responsibilities": "Assert that GPT-2 is racist"
    },
    {
      "[id_2]": 6,
      "[id_1]": 2,
      "[id_0]": 1,
      "experience.responsibilities": "Assert that GPT-3 is racist"
    },
    {
      "[id_2]": 7,
      "[id_1]": 2,
      "[id_0]": 1,
      "experience.responsibilities": "Develop a prototype of a premium non-racist language model"
    }
  ]
]
```

Each element of the output is a list of flat dictionaries, and therefore be thought of as tables. In this example these 
three tables represent, in order, persons, jobs, and job responsibilities.

Let's proceed by using Pandas to convert each of element of the output into a DataFrame and do some renaming:

```
import pandas as pd

dfs = [pd.DataFrame(t) for t in tables]

id_map = {
    "[id_0]": "person_id",
    "[id_1]": "job_id",
    "[id_2]": "responsibility_id"
}

for df in dfs:
    df.rename(columns=id_map, inplace=True)
    df.set_index(df.columns[0], inplace=True)

df_person, df_job, df_responsibility = dfs

df_job.rename(columns={x: x.replace("experience.", "") for x in df_job.columns if "experience."}, inplace=True)
df_responsibility.rename(columns={"experience.responsibilities": "responsibility"}, inplace=True)

for df in dfs:
    print(df.to_markdown(), "\n")
```

| person_id | name  | age |
|----------:|:------|----:|
|         0 | Alice |  34 |
|         1 | Bob   |  27 | 

| job_id | person_id | company  | role                  | from |   to |
|-------:|----------:|:---------|:----------------------|-----:|-----:|
|      0 |         0 | Google   | Software Engineer     | 2020 | 2022 |
|      1 |         0 | Facebook | Senior Data Scientist | 2017 | 2020 |
|      2 |         1 | OpenAI   | NLP Engineer          | 2019 | 2022 | 

| responsibility_id | job_id | person_id | responsibility                                             |
|------------------:|-------:|----------:|:-----------------------------------------------------------|
|                 0 |      0 |         0 | Google stuff                                               |
|                 1 |      0 |         0 | Mark TensorFlow issues as "Won't Do"                       |
|                 2 |      1 |         0 | Censor media                                               |
|                 3 |      1 |         0 | Learn the foundations of ML                                |
|                 4 |      1 |         0 | Do Kaggle competitions                                     |
|                 5 |      2 |         1 | Assert that GPT-2 is racist                                |
|                 6 |      2 |         1 | Assert that GPT-3 is racist                                |
|                 7 |      2 |         1 | Develop a prototype of a premium non-racist language model | 
