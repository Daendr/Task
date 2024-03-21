# This image prepares war-container with ready application
FROM maven:3.5.3-jdk-8 as builder

# Defining args for reading from docker-compose file
ARG GIT_USR
ARG GIT_PWD

# Defining environment variables
ENV PROJECT_NAME task-sources
ENV GIT_USR "$GIT_USR"
ENV GIT_PWD "$GIT_PWD"
ENV GIT_DOMAIN github.com
ENV GIT_PROJECT_PATH tquality-education-exam/$PROJECT_NAME.git
ENV GIT_REPO=https://$GIT_USR:$GIT_PWD@$GIT_DOMAIN/$GIT_PROJECT_PATH

# Creating working directory for Maven
RUN mkdir -p "$MAVEN_HOME"
WORKDIR $MAVEN_HOME

# Updating sources.list file
RUN sed -i 's/deb.debian.org/archive.debian.org/g' /etc/apt/sources.list
RUN sed -i 's|security.debian.org|archive.debian.org/|g' /etc/apt/sources.list
RUN sed -i '/stretch-updates/d' /etc/apt/sources.list

# Installing Git
RUN apt-get -y update && apt-get -y install git

# Cloning project repository
RUN git clone $GIT_REPO

# Packaging project into war-containers
RUN mvn clean package -f ${MAVEN_HOME}/${PROJECT_NAME}/pom.xml

# This image deploying application on Tomcat
FROM tomcat:7-jre8

# Defining environment variables
ENV PROJECT_NAME task-sources
ENV MODULE_NAME_DB union_reporting
ENV MODULE_NAME union-reporting
ENV TOMCAT_USER login
ENV TOMCAT_PASSWORD password
ENV TOMCAT_ROLE testportalrole
ENV DB_PORT 3306
ENV DB_URL jdbc:mysql://db:${DB_PORT}/${MODULE_NAME_DB}

ENV TOMCAT_USERS_XML <role rolename="\"${TOMCAT_ROLE}\""/> <user username="\"${TOMCAT_USER}\"" password="\"${TOMCAT_PASSWORD}\"" roles="\"${TOMCAT_ROLE}\""/> </tomcat-users>
ENV TOMCAT_CONTEXT_XML <WatchedResource>WEB-INF/web.xml</WatchedResource> <Resource name='"jdbc/mysql"' auth='"Container"' type='"javax.sql.DataSource"' maxTotal='"100"' maxIdle='"30"' maxWaitMillis='"10000"' username="\"${TOMCAT_USER}\"" password="\"${TOMCAT_PASSWORD}\"" driverClassName='"com.mysql.jdbc.Driver"' url="\"${DB_URL}\""/> </Context>

# Setting maintainer for the image
MAINTAINER Artyom Ryazantsev

# Creating working directory for Tomcat
RUN mkdir -p "$CATALINA_HOME"
WORKDIR $CATALINA_HOME

# Deleting default ROOT-app on Tomcat
RUN rm -r ${CATALINA_HOME}/webapps/ROOT

# Updating sources.list file
RUN sed -i 's/deb.debian.org/archive.debian.org/g' /etc/apt/sources.list
RUN sed -i 's|security.debian.org|archive.debian.org/|g' /etc/apt/sources.list
RUN sed -i '/stretch-updates/d' /etc/apt/sources.list

# Installing rpl tool
RUN apt-get update && apt-get -y install rpl

# Replacing required configuration data on Tomcat
RUN rpl '</tomcat-users>' "${TOMCAT_USERS_XML}" ${CATALINA_HOME}/conf/tomcat-users.xml
RUN rpl '</Context>' "${TOMCAT_CONTEXT_XML}" ${CATALINA_HOME}/conf/context.xml

# Deploying the application (web and api parts) on Tomcat
COPY --from=builder /usr/share/maven/${PROJECT_NAME}/${MODULE_NAME}-api/target/api.war ${CATALINA_HOME}/webapps/api.war
COPY --from=builder /usr/share/maven/${PROJECT_NAME}/${MODULE_NAME}-web/target/web.war ${CATALINA_HOME}/webapps/web.war

EXPOSE 8080

CMD ["catalina.sh" , "run"]
