# Бекенд сервиса для отслеживания динамики курса рубля 


Для запуска ПО вам понадобятся консольный Git, Docker и Docker Compose. Инструкции по их установке ищите на официальных сайтах:

- [Install Docker Desktop](https://www.docker.com/get-started/)
- [Install Docker Compose](https://docs.docker.com/compose/install/)

> Для тех, кто использует Windows необходимы также программы **git** и **git bash**. В git bash надо добавить ещё команду make:
>
> - Go to [ezwinports](https://sourceforge.net/projects/ezwinports/files/)
> - Download make-4.2.1-without-guile-w32-bin.zip (get the version without guile)
> - Extract zip
> - Copy the contents to C:\ProgramFiles\Git\mingw64\ merging the folders, but do NOT overwrite/replace any exisiting files.
>
> Все дальнейшие команды запускать из-под **git bash**

Для первоначального запуска процесса необходимо выполнить команду 

```shell
$ # Запуск проекта (после сборки)
$ make first_start
```

При этом на компьютер будут скачены все необходимые образы и проведены необходимые миграции

Далее для использования запустить и не выключать процесс

```shell
$ docker compose up
```