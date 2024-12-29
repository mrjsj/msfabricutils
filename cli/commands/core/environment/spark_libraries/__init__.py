from cyclopts import App

from .cancel_publish import cancel_publish_command
from .delete_staging_library import delete_staging_library_command
from .get_published_libraries import get_published_libraries_command
from .get_staging_libraries import get_staging_libraries_command
from .publish_environment import publish_environment_command
from .upload_staging_library import upload_staging_library_command

spark_libraries_app = App(name="spark-libraries", help="[yellow]Commands for spark_libraries[/yellow]")
spark_libraries_app.command(cancel_publish_command, name="cancel-publish")
spark_libraries_app.command(delete_staging_library_command, name="delete-staging-library")
spark_libraries_app.command(get_published_libraries_command, name="get-published-libraries")
spark_libraries_app.command(get_staging_libraries_command, name="get-staging-libraries")
spark_libraries_app.command(publish_environment_command, name="publish-environment")
spark_libraries_app.command(upload_staging_library_command, name="upload-staging-library")
