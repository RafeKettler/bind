from bind import API, Request
from bind.callbacks import response_to_json, request_to_formdata

class GithubAPI(API):
    BASE_URL = "https://github.com/api/v2/json"
    RESPONSE_CALLBACK = response_to_json
    get_user_data = Request("/user/show/:user", "GET")
    get_user_data_extra = Request("/user/show", "GET", requires_auth=True)
    comment_on_issue = Request("/issues/comment/:user/:repo/:id", "POST",
                               request_callback=request_to_formdata,
                               requires_auth=True)

if __name__ == '__main__':
    gh = GithubAPI()
    gh.authenticate("<username>", "<password>")
    comment = {"comment":"test comment"}
    print gh.comment_on_issue(comment, repo="somerepo", id="someid")

