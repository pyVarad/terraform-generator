## Terraform Generator

The utility is to consume cf2tf and az2tf generators to create corresponding terraform templates. 

Setup needs a `.env` file within the `tf_generator` folder.

```dotenv
ENV_STATE=dev
DEV_DATABASE_URL=sqlite+aiosqlite:///data.db
```

There is no use of database at this point of time however just added as a placeholder for future upgrades.


Start the server using the command.
```shell
uvicorn main:app --reload
```

Use the swagger to explpre the [api](http://localhost:8000/docs)