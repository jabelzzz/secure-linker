Used technologies
* Python
* FastAPI
* Secrets for the token generation
* Uvicorn as WSGI
* PostgreSQL to save the generated URLs

## Database Configuration

Make sure to define the `DATABASE_URL` environment variable with your PostgreSQL connection string.

### Locally
- Create a `.env` file in the root of the project (if it doesn't exist).
- Add the following line, replacing the values with your local or Railway public connection string:

	```
	DATABASE_URL=postgresql://user:password@host:port/db_name
	```

- Example for local PostgreSQL:
	```
	DATABASE_URL=postgresql://postgres:yourpassword@localhost:5432/securelinker
	```

The project already includes automatic loading of environment variables using `python-dotenv`. No extra steps are needed.

Tables are created automatically at application startup if they do not exist, thanks to SQLAlchemy.

---

## Automatic Cleanup of Expired Links

The project includes a script to remove expired links or those with no remaining views from the database.

### Manual Usage

You can run the script manually with:

```sh
export DATABASE_URL=postgresql://user:password@host:port/db_name
python src/secure_linker/utils/clean_expired_links.py
```

This will delete all links that have expired by date or have exhausted their allowed views.

**Note:**
Make sure the `DATABASE_URL` variable is correctly set before running the script.