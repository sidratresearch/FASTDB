import subprocess
import uuid
from pathlib import Path
from typing import Annotated

import typer
import yaml
from db import AuthUser, BaseProcessingVersion, DBCon, ProcessingVersion
from util import asUUID

app = typer.Typer(
    no_args_is_help=True,
    add_completion=False,
    help="Functions to simplify running FASTDB in a development mode (for testing external integrations)",
)

user = AuthUser(
    id=asUUID("788e391e-ca63-4057-8788-25cc8647e722"),
    username="test",
    displayname="test user",
    email="test@nowhere.org",
    pubkey="""-----BEGIN PUBLIC KEY-----
            MIICIjANBgkqhkiG9w0BAQEFAAOCAg8AMIICCgKCAgEA1QLihZJ78NHKppUBUaZI
            sel7WFKp/3Pr14nbel+BpfOVWrIIIiMegQSAliWRszNLQezKwHTXM4DUxZu7LG/q
            zut37v5WSVWCK8wSW+zy6e9vnuVkcrzdEJgkztUaiC8lMnHVE0ycpLTICcAu0wtv
            WP32ScyNbiHidyPZwNd9XB4juLl9j7K6hs7WQwmeMOyw8dUZuE8b/jiHrAxxnHjE
            Sli8bjR7I6X3AX8U81bP4qFjTjGuy85dIeZEbyS6UpbmkZ+imr/0wLa9knRoW0hU
            Uz8p+P/Vts3rimpQtPajtRzCpTY4lRfh05YDmr2rc1WHJ/IPu3v7sIUg8K/egoPJ
            VU3c2QYGpwmpnldbb+bpSUXxpsQVtFw5pHmqEbfKXWNM8CTkii8s6bI03/JQREBU
            L3OzCGclvS8lQ+ZXAQaMyjshMqMFud3E9RS5EFxpSfk92r+RY7PgaYs9PX7x33zU
            k/937nk7sTR5OEKFgxRDx61svk5UJIPQib5SnIDRNAqeKhxg23q5ZqDMBVk1rAhI
            xFuX4Hj8VtG89J3DSVJue4psF0wTYceUhUleJCG3gPxAyE2g4ObZZ9mh/gI1KG6v
            Np9CFWk9eMSeehEI1YKyPY8Hdv50PmIvN2zgxbo2wccspwCVTrtdKoQebpVAAu3v
            tyOci9saPPfI1bNnKD202zsCAwEAAQ==
            -----END PUBLIC KEY-----
            """,
    privkey={
        "iv": "z84DFtRURdKFhn3b",
        "salt": "57B2Nq/ZToHhVM+1DEq30g==",
        "privkey": "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",
    },  # noqa: E501
)


postgres_username = "postgres"
postgres_hostname = "postgres"
postgres_database = "fastdb"
pgpass_path = Path("~/.pgpass").expanduser()


def enable_psql_access() -> None:
    hostname, username, database = (
        postgres_hostname,
        postgres_username,
        postgres_database,
    )
    port = "*"
    password = "fragile"
    pgpass_path.write_text(f"{hostname}:{port}:{database}:{username}:{password}")
    pgpass_path.chmod(0o600)  # 0o for octal literal, 600 for rw- --- ---


def populate_processing_versions() -> None:
    with DBCon() as con:
        # first part of the fixture is just checking that it's not trying to
        # duplicate things. May want to do this as well, later on

        tables = [
            "diaobject",
            "diaobject_position",
            "diasource",
            "diaforcedsource",
            "host_galaxy",
        ]
        bases = ["bpv1", "bpv1a", "realtime"]
        procver_postimes = [
            60000,
            60030,
            60050,
            60060,
            60080,
        ]  # MJDs of positions used by procver_collection and set_of_lightcurves.

        bpvs = {}
        pvs = {}

        for base in bases:
            for table in tables:
                if table == "diaobject_position":
                    for postime in procver_postimes:
                        # uuiddex += 1
                        key = f"{base}_diaobject_position_{postime}"
                        desc = (
                            f"{base}_{postime}"
                            if base == "realtime"
                            else f"pvc_{base}_{postime}"
                        )
                        bpvs[key] = BaseProcessingVersion(
                            # id=uuidbatch[uuiddex],
                            id=uuid.uuid4(),
                            _table=table,
                            description=desc,
                        )
                else:
                    # uuiddex += 1
                    key = f"{base}_{table}"
                    desc = base if base == "realtime" else f"pvc_{base}"
                    bpvs[key] = BaseProcessingVersion(
                        # id=uuidbatch[uuiddex],
                        id=uuid.uuid4(),
                        _table=table,
                        description=desc,
                    )

        for bpv in bpvs.values():
            bpv.insert(dbcon=con, nocommit=True, refresh=False)

        pvs["pv1"] = ProcessingVersion(id=uuid.uuid4(), description="pvc_pv1")
        # pvs["pv2"] = ProcessingVersion(id=uuid.uuid4(), description="pvc_pv2")
        # pvs["pv3"] = ProcessingVersion(id=uuid.uuid4(), description="pvc_pv3")
        pvs["realtime"] = ProcessingVersion(id=uuid.uuid4(), description="realtime")

        for pv in pvs.values():
            pv.insert(dbcon=con, nocommit=True, refresh=False)

        pvinfo = []

        for pv, bpvae in zip(
            ["pv1", "realtime"],
            [["bpv1", "bpv1a"], ["realtime"]],
        ):
            thisinfo = {"procver": pvs[pv]}

            print(f"\n{pv=} {bpvae=} {thisinfo=}")

            for prio, bpv in enumerate(bpvae):
                print(f"{prio=} {bpv=}")
                for table in tables:
                    print(f"\t{table=}")
                    if table not in thisinfo:
                        thisinfo[table] = []
                    if table == "diaobject_position":
                        for posn, postime in enumerate(procver_postimes):
                            # I know that there are never more than 10 bpvs for a given pv
                            subprio = prio * 10 + posn
                            bpvkey = f"{bpv}_diaobject_position_{postime}"
                            con.execute_nofetch(
                                "INSERT INTO base_procver_of_procver(procver_id,base_procver_id,"
                                "                                    _table,priority) "
                                "VALUES (%(pv)s,%(bpv)s,%(tab)s,%(prio)s)",
                                {
                                    "pv": pvs[pv].id,
                                    "bpv": bpvs[bpvkey].id,
                                    "tab": table,
                                    "prio": subprio,
                                },
                            )
                            print(
                                f"\t\tUpdating base_procver_of_procver for {postime=} with: {{pv={pvs[pv].id}, bpv={bpvs[bpvkey].id}, tab={table}, prio={subprio}}}",
                            )
                            thisinfo[table].append((bpvs[bpvkey], subprio, bpvkey))
                    else:
                        bpvkey = f"{bpv}_{table}"
                        con.execute_nofetch(
                            "INSERT INTO base_procver_of_procver(procver_id,base_procver_id,"
                            "                                    _table,priority) "
                            "VALUES (%(pv)s,%(bpv)s,%(tab)s,%(prio)s)",
                            {
                                "pv": pvs[pv].id,
                                "bpv": bpvs[bpvkey].id,
                                "tab": table,
                                "prio": prio,
                            },
                        )
                        print(
                            f"\t\tUpdating base_procver_of_procver  with: {{pv={pvs[pv].id}, bpv={bpvs[bpvkey].id}, tab={table}, {prio=}}}",
                        )
                        # This is becoming an increasingly ugly hack.  This is what happens
                        #  when you really need to get things done but should really
                        #  be refactoring previous mistakes.
                        thisinfo[table].append((bpvs[bpvkey], prio, bpvkey))

            # Reverse all the table lists so they go from high prio to low prio
            for table in thisinfo.keys():
                if table == "procver":
                    continue
                thisinfo[table].reverse()

            pvinfo.append(thisinfo)

        # we aren't using "pv2"
        # con.execute_nofetch(
        #     "INSERT INTO processing_version_alias(description,procver_id) "
        #     "VALUES ('default',%(pvid)s)",
        #     {"pvid": pvs["pv2"].id},
        # )

        print(f"{bpvs.keys()=}")
        print(f"{pvs.keys()=}")
        """
        pvinfo is a list of dicts, which maps base processing versions to processing versions
        it has length equal to the number of processing versions
        
        each dict has a key "procver" which is the non-base processing version being linked to
        and also a key for each table type (diaobject, diasource, etc.)
        those table keys have list values
        and the list is of (base processing version, priority, base processing version key)
        """

        con.commit()

        """
        SELECT * FROM base_processing_version; # 27 rows
        SELECT * FROM base_procver_of_procver; # 27 rows
        SELECT * FROM processing_version; # 2 rows
        SELECT * FROM processing_version_alias; # 0 rows

        was then able to run source_importer with
        -o realtime -p realtime_60000 -s realtime -f realtime

        webui still having issues
        - show random obj: 'list' object has no attribute 'keys'
        - if I copy in a specific diaobjectid from the diaobject postgres table there's a console error: can't access property "s/n", this.data.ltcv is undefined
        """


def clear_processing_versions() -> None:
    with DBCon() as con:
        con.execute_nofetch("DELETE FROM base_procver_of_procver")
        con.execute_nofetch("DELETE FROM processing_version_alias")
        con.execute_nofetch("DELETE FROM processing_version ")
        con.execute_nofetch("DELETE FROM base_processing_version")
        con.commit()


@app.command()
def setup() -> None:
    """[First][Once] Set up a test user, processing versions, and other things to allow easily working with FASTDB."""
    if pgpass_path.exists():
        raise ValueError("pgpass file exists, `setup` was probably run already")
    user.insert()
    populate_processing_versions()
    enable_psql_access()

    print("\n\nSuccessfully set up FASTDB for use.\n")


@app.command(no_args_is_help=True)
def run_broker_consumer(
    config_file: Annotated[
        Path,
        typer.Argument(
            help="Path to brokerconsumer config YAML",
            exists=True,
            file_okay=True,
            dir_okay=False,
            readable=True,
            resolve_path=True,
        ),
    ],
) -> None:
    """[After `setup`] Poll a broker for alerts.
    You will likely want to let this run for a little bit, keeping an eye on the number of messages handled, then quit with CTRL-c
    It may take a few seconds for the script to clean up and exit
    May also need to hit CTRL-c again when you see "Exiting BrokerConsumerLauncher"
    """
    subprocess.run(
        f"python /fastdb/services/brokerconsumer.py {str(config_file)}",
        shell=True,
    )


@app.command(no_args_is_help=True)
def run_source_importer(
    config_file: Annotated[
        Path,
        typer.Argument(
            help="Path to brokerconsumer config YAML (same one used for `run-broker-consumer`)",
            exists=True,
            file_okay=True,
            dir_okay=False,
            readable=True,
            resolve_path=True,
        ),
    ],
    processing_version: Annotated[
        str,
        typer.Option(
            help="Processing version to import alerts with. Needs to exist in the base_processing_version table."
        ),
    ] = "realtime",
    position_MJD: Annotated[
        int,
        typer.Option(
            help="An MJD to use in the processing version of diaobject_position entries. Needs to have been used already when populating the base_processing_version table."
        ),
    ] = 60000,
) -> None:
    """[After `run-broker-consumer`] Run the source_importer script to move alerts from a MongoDB collection to the Postgres tables."""
    base_processing_versions = {
        "object": processing_version,
        "object-position": f"{processing_version}_{position_MJD}",
        "source": processing_version,
        "forcedsource": processing_version,
    }

    config_yaml = yaml.safe_load(config_file.read_text())
    collections = [
        broker_config["mongodb_collection_base"]
        for broker_config in config_yaml["brokers"].values()
    ]
    print(f"Importing from MongoDB collections: {collections}")


    subprocess.run([
        "python",
        "/fastdb/services/source_importer.py",
        "--collection",
        *collections,
        "-o",
        base_processing_versions["object"],
        "-p",
        base_processing_versions["object-position"],
        "-s",
        base_processing_versions["source"],
        "-f",
        base_processing_versions["forcedsource"],
    ])


@app.command()
def dump_diaobjectids() -> None:
    """[After `run-source-importer`] Dump all known diaobjectids into a csv file."""
    csv_path = "../test-scripts/diaobjectids.csv"  # relative to the FASTDB repo, on the host machine
    psql_command = "SELECT diaobjectid FROM diaobject;"
    subprocess.run(
        [
            "psql",
            f"--username={postgres_username}",
            f"--host={postgres_hostname}",
            f"--dbname={postgres_database}",
            "--csv",
            "--tuples-only",
            f"--output={csv_path}",
            f"--command={psql_command}",
        ]
    )
    with open(csv_path, "rb") as f:
        num_lines = sum(1 for _ in f)
    print(f"{num_lines} lines written to {csv_path}")


@app.command()
def teardown() -> None:
    """[Last][Once] Undo the actions from `setup`."""
    user.delete_from_db()
    clear_processing_versions()
    pgpass_path.unlink()

    print(
        "\n\nSuccessfully cleaned up FASTDB configuration. Database dumps and alert tables have not been modified. Stop and start the docker containers to get a fully clean environment.\n"
    )


if __name__ == "__main__":
    app()
