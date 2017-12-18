echo "Running Build ID: ${env.BUILD_ID}"

string githubUrl
String appName
String build_args
String deployLogin
String docker_img_name
def docker_img

node {

    deleteDir()

    stage("parameters") {
        //
        // Parameters passed through from the Jenkins Pipeline configuration
        //
        string(name: 'deploymentServer',
               description: 'Server to deploy the Docker container',
               defaultValue: '*')
        string(name: 'deploymentUsername',
               description: 'Username for the server the Docker container will be deployed to (used for ssh/scp)',
               defaultValue: '*')
        string(name: 'portApplication',
               description: 'Port number used by application to expose APIs on',
               defaultValue: '*')
        string(name: 'fileConfig',
               description: 'Location of config file on host device',
               defaultValue: '*')
        string(name: 'folderLog',
               description: 'Location of log directory on host device',
               defaultValue: '*')
        //
        githubUrl = "https://github.com/robe16/jarvis.tv_lg_netcast.git"
        appName = "jarvis.tv_lg_netcast"
        //
        build_args = ["--build-arg portApplication=${portApplication}"].join(" ")
        //
        //
        docker_volumes = ["-v ${params.fileConfig}:/jarvis/nest/config/config.json",
                          "-v ${params.folderLog}:/jarvis/nest/log/logfiles/"].join(" ")
        //
        //
        deployLogin = "${params.deploymentUsername}@${params.deploymentServer}"
        //
    }

    if (params["deploymentServer"]!="*" && params["deploymentUsername"]!="*" && params["portMapped_broadcast"]!="*" && params["portMapped_application"]!="*" && params["fileConfig"]!="*" && params["folderLog"]!="*") {

        stage("checkout") {
            git url: "${githubUrl}"
            sh "git rev-parse HEAD > .git/commit-id"
        }

        docker_img_name_build_id = "${appName}:${env.BUILD_ID}"
        docker_img_name_latest = "${appName}:latest"

        stage("build") {
            try {sh "docker image rm ${docker_img_name_latest}"} catch (error) {}
            sh "docker build -t ${docker_img_name_build_id} ${build_args} ."
            sh "docker tag ${docker_img_name_build_id} ${docker_img_name_latest}"
        }

        stage("deploy"){
            //
            String docker_img_tar = "docker_img.tar"
            //
            try {
                sh "rm ~/${docker_img_tar}"                                                                 // remove any old tar files from cicd server
            } catch(error) {
                echo "No ${docker_img_tar} file to remove."
            }
            sh "docker save -o ~/${docker_img_tar} ${docker_img_name_build_id}"                             // create tar file of image
            sh "scp -v -o StrictHostKeyChecking=no ~/${docker_img_tar} ${deployLogin}:~"                    // xfer tar to deploy server
            sh "ssh -o StrictHostKeyChecking=no ${deployLogin} \"docker load -i ~/${docker_img_tar}\""      // load tar into deploy server registry
            sh "ssh -o StrictHostKeyChecking=no ${deployLogin} \"rm ~/${docker_img_tar}\""                  // remove the tar file from deploy server
            sh "rm ~/${docker_img_tar}"                                                                     // remove the tar file from cicd server
            // Set 'latest' tag to most recently created docker image
            sh "ssh -o StrictHostKeyChecking=no ${deployLogin} \"docker tag ${docker_img_name_build_id} ${docker_img_name_latest}\""
            //
        }

        stage("start container"){
            // Stop existing container if running
            sh "ssh ${deployLogin} \"docker rm -f ${appName} && echo \"container ${appName} removed\" || echo \"container ${appName} does not exist\"\""
            // Start new container
            sh "ssh ${deployLogin} \"docker run --restart unless-stopped -d ${docker_volumes} --net=host --name ${appName} ${docker_img_name_latest}\""
            //sh "ssh ${deployLogin} \"docker run --restart unless-stopped -d ${docker_volumes} ${docker_port_mapping} --name ${appName} ${docker_img_name_latest}\""
        }

    } else {
        error("Build cancelled as required parameter values not provided by pipeline configuration")
    }

}