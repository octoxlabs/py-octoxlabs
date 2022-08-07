# py-octoxlabs Development and Contribution

1. Open issue in [https://github.com/octoxlabs/py-octoxlabs/issues/new](https://github.com/octoxlabs/py-octoxlabs/issues/new)
2. Clone this repository *command1
3. Create new branch with your issue id *command2
4. Install Requirements *command3
5. Make your changes
6. Write your tests
7. Install pre-commit *command4
8. Commit and push your changes *command5
9. Create new pull request in [https://github.com/octoxlabs/py-octoxlabs/pulls](https://github.com/octoxlabs/py-octoxlabs/pulls)


## Commands
### command1
```shell
git clone git@github.com:octoxlabs/py-octoxlabs.git
```

### command2
```shell
git checkout -b feature-#<issue-id>
# or
git checkout -b hotfix-#<issue-id>
```

### command3
```shell
pip install -r requirements/development.txt
```

### command4
```shell
pre-commit install
```

### command5
```shell
git add .
pre-commit run  # check pre-commit
git commit -m "added changes #<issue-id>"
git push origin feature-#<issue-id>
```