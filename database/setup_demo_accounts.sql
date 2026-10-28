/*
    Настройка демонстрационных пользователей Narra.
    Выполнять от имени администратора SQL Server.
    Перед запуском заменить все пароли-заглушки.
*/

USE [master];
GO

CREATE LOGIN [content_viewer]
WITH PASSWORD = N'<REPLACE_WITH_VIEWER_PASSWORD>',
     CHECK_POLICY = ON;
GO

CREATE LOGIN [content_editor]
WITH PASSWORD = N'<REPLACE_WITH_EDITOR_PASSWORD>',
     CHECK_POLICY = ON;
GO

CREATE LOGIN [project_admin]
WITH PASSWORD = N'<REPLACE_WITH_ADMIN_PASSWORD>',
     CHECK_POLICY = ON;
GO

USE [NarraDB];
GO

CREATE USER [content_viewer] FOR LOGIN [content_viewer];
ALTER ROLE [db_datareader] ADD MEMBER [content_viewer];
GO

CREATE USER [content_editor] FOR LOGIN [content_editor];
ALTER ROLE [db_datareader] ADD MEMBER [content_editor];
ALTER ROLE [db_datawriter] ADD MEMBER [content_editor];
GO

CREATE USER [project_admin] FOR LOGIN [project_admin];
ALTER ROLE [db_owner] ADD MEMBER [project_admin];
GO