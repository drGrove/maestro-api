/********************
* High Level Setup  *
********************/
local pipeline(
  name,
  kind = "pipeline",
  type = "docker",
  clone = null,
  platform = null,
  workspace = null,
  services = [],
  steps = [],
  trigger = null,
  node = null,
  volumes = [],
  depends_on = [],
) = {
  kind: kind,
  type: type,
  name: name,
  [if platform != null then 'platform']: platform,
  [if workspace != null then 'workspace']: workspace,
  [if clone != null then 'clone']: clone,
  [if services != [] then 'services']: services,
  [if steps != [] then 'steps']: steps,
  [if trigger != null then 'trigger']: trigger,
  [if node != null then 'node']: node,
  [if volumes != [] then 'volumes']: volumes,
  [if depends_on != [] then 'depends_on']: depends_on,
};

local step(
  name,
  image,
  settings = null,
  depends_on = [],
  commands = [],
  environment = null,
  failure = false,
  detach = false,
  privileged = false,
  volumes = [],
  when = null
) = {
  name: name,
  image: image,
  [if failure then 'failure']: "ignore",
  [if detach then 'detach']: detach,
  [if privileged then 'privileged']: detach,
  [if settings != null then 'settings']: settings,
  [if depends_on != [] then 'depends_on']: depends_on,
  [if commands != [] then 'commands']: commands,
  [if environment != null then 'environment']: environment,
  [if volumes != [] then 'volumes']: volumes,
  [if when != null then 'when']: when,
};

/********************
* Global Variables  *
********************/
local service_postgres = {
  name: "postgres",
  image: "postgres:11.2",
  environment: {
    POSTGRES_USER: "postgres",
    POSTGRES_PASSWORD: "postgres",
    POSTGRES_DB: "maestro",
  },
};

// local volumes = [
//   {
//     name: "docker-socket",
//     host: {
//       path: "/var/run/docker.sock"
//     },
//   },
// ];

// local mounts = [
//   {
//     name: "docker-socket",
//     path: "/var/run/docker.sock",
//   },
// ];



[
  pipeline(
    name = "build",
    // volumes = volumes,
    steps = [
      step(
        name = "build",
        image = "docker:stable-git",
        commands = [
          "apk add make",
          "make build-image"
        ],
      ),
      step(
        name = "tag",
        image = "docker:stable-git",
        commands = [
          "apk add make",
          "make tag-image-latest"
        ],
        depends_on = [
          "build"
        ],
        when = {
          ref: {
            includes: [
              "master"
            ]
          }
        }
      ),
      step(
        name = "publish",
        image = "docker:stable-git",
        commands = [
          "apk add make",
          "make push-image",
        ],
        depends_on = [
          "build"
        ]
      )
    ]
  ),
  pipeline(
    name = "test",
    services = [
      service_postgres,
    ],
    // volumes = volumes,
    steps = [
      step(
        name = "setup",
        image = "python:3.8-buster",
        commands = [
          "apt-get install make",
          "make setup"
        ]
      ),
      step(
        name = "lint",
        image = "python:3.8-buster",
        commands = [
          "apt-get install make",
          "make lint",
        ],
        depends_on = [
          "setup"
        ],
      ),
      step(
        name = "unit-tests",
        image = "python:3.8-buster",
        commands = [
          "apt-get install make",
          "make test",
        ],
        environment = {
          SQLALCHEMY_DATABASE_URI: "postgresql://postgres:postgres@postgres/maestro"
        },
        depends_on = [
          "setup"
        ],
      ),
      step(
        name = "coverage",
        image = "python:3.8-buster",
        commands = [
          "apt-get install make",
          "make setup",
          "make coverage"
        ],
        environment = {
          COVERALLS_REPO_TOKEN: {
            from_secret: "COVERALLS_REPO_TOKEN",
          },
        },
      ),
    ]
  )
]
