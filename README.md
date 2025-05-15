## Install or add required dependencies using uv 
```bash 
uv sync
```

### set anthropic api key in your terminal environment
```bash
set ANTHROPIC_API_KEY=<your-key>
```

## Create .env file
- add required environment variables from ```.env.template``` file


### run app 
```bash
uvicorn app.main:app --reload
```


## Example

send post request on ```/agent``` route with below request body 

```json 
{
  "prompt" : "User promt/query",
  "user_email" : "recipent_email@example.com" 
}
```

You should recieve response as pdf on email given in ```user_email```.

### request sent on ```/agent``` route
![image](https://github.com/user-attachments/assets/fbd5e3b9-b3c6-44f0-a6b3-58eb6e10ad87)

### generated pdf
[output.pdf](https://github.com/user-attachments/files/20162036/output.pdf)


### received response on email with attached pdf
![image](https://github.com/user-attachments/assets/f265240b-8329-4452-8c0a-82fa3b2dae25)





