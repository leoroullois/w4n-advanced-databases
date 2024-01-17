FROM postgres

# install citus
RUN apt-get update && apt-get install -y curl
RUN curl https://install.citusdata.com/community/deb.sh > add-citus-repo.sh
RUN bash add-citus-repo.sh
RUN apt-get -y install postgresql-16-citus-12.1

# command: postgres -c shared_preload_libraries="pg_stat_statements" -c pg_stat_statements.track=all -c max_connections=200

CMD ["postgres", "-c", "shared_preload_libraries=citus,pg_stat_statements", "-c", "pg_stat_statements.track=all", "-c", "max_connections=200"]

