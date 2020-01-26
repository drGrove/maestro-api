package deploy

import (
	"database/sql"

	"github.com/drGrove/maestro/proto"
)

type Deploy struct {
	Id int64
	Status DeployStatus
	BuildId int64
	Repo string
}

func (deploy *Deploy) Save(db *sql.DB) Deploy, error {
	_, err := db.Exec(
		`
			INSERT INTO
				maestro.public.deploy
			(build_id, repo)
			VALUES
			($1, $2)
		`,
		deploy.BuildId, deploy.Repo
	)
	if err != nil {
		return nil, err
	}
	return deploy, nil
}

func (deploy *Deploy) ToPB() *deploy.Deploy {
	return &deploy.Deploy {

	}
}
