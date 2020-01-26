package server;

import (
	"context"
	"time"

	"github.com/drGrove/maestro/proto"
	"github.com/golang/protobuf/ptypes"
	"github.com/google/uuid"
	log "github.com/sirupsen/logrus"
	"google.golang.org/grpc/codes"
	"google.golang.org/grpc/status"
)

type MaestroServer struct {
}

func (s *MaestroServer) CreateDeploy(ctx context.Context, req *deploy.CreateDeployRequest) (*deploy.Deploy, error) {



	// newTimerID := uuid.New().String()
	// go func(id string, dur time.Duration) {
	// 	timer := time.NewTimer(dur)
	// 	<-timer.C
	// 	log.Infof("Timer %s time!", newTimerID)
	// }(newTimerID, when.Sub(time.Now()))

	// return &reminder.ScheduleReminderResponse{
	// 	Id: newTimerID,
	// }, nil
}
