# Youtube Analysis Using NLP

## Installation

`python -m venv env`

Open terminal. You should see (env). Then

`pip install -r requirements.txt`

---

## After Installation

- Copy `.env` file to directory having `youtube.py`

  ```bash
  KEY=
  ```

- Open terminal. U should see a (env) symbol
- Run the code by `python youtube.py`

---

## Generate comments & captions

- Set `videoId` and `TESTING = False` in `youtube.py`
- Run the code by `python youtube.py`
- This will generate the comments and captions in '/data' folder

---

## Model Generation

### SpamDetection

```python
  # Set retrain_model as True
  spamDetector = SpamDetection(retrain_model=True)
```

- Run the code `python youtube.py`
- This will generate the data sets in `model/spam/data` folder
