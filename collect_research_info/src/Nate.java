package edu.ksu.canvas;

import edu.ksu.canvas.interfaces.QuizReader;
import edu.ksu.canvas.interfaces.SubmissionReader;
import edu.ksu.canvas.model.User;
import edu.ksu.canvas.model.assignment.*;
import edu.ksu.canvas.oauth.NonRefreshableOauthToken;
import edu.ksu.canvas.oauth.OauthToken;
import edu.ksu.canvas.requestOptions.GetSubmissionsOptions;

import java.io.FileWriter;
import java.io.IOException;
import java.util.ArrayList;
import java.util.List;

public class Nate {
    public static void main(String[] args) throws IOException {

        String canvasUrl = "";
        String token = "";
        String courseId = "";

        String[] letters = {"B", "C", "D"};

        for (String letter : letters) {
            String quiz1 = "Recursion Practice "+letter+"1";
            String quiz2 = "Recursion Practice "+letter+"2 revisited";

            List<List<String>> comments1 = getQuiz(canvasUrl, token, courseId, quiz1);
            List<List<String>> comments2 = getQuiz(canvasUrl, token, courseId, quiz2);
            int userName = 0;
            int sisUserId = 1;
            int commentAuthor = 2;
            int comment = 3;
            int score = 4;

            // Define the file path

            String filePath1 = "Vicki_Comments_"+letter+"1.csv";
            String filePath2 = "Vicki_Comments_"+letter+"2.csv";
            String delimiter = ",";
            String lineEnd = "\n";

            try {
                // Create a FileWriter object
                FileWriter fileWriter1 = new FileWriter(filePath1);
                FileWriter fileWriter2 = new FileWriter(filePath2);
                fileWriter1.write("UserName"+delimiter+"sisUserId"+delimiter+"submissionScore"+delimiter+"submissionComment"+delimiter+"submissionCommentAuthor"+lineEnd);
                for (List<String> data : comments1) {
                    fileWriter1.write(cleanString(data.get(userName))+delimiter+cleanString(data.get(sisUserId))+delimiter+cleanString(data.get(score))+delimiter+cleanString(data.get(comment))+delimiter+cleanString(data.get(commentAuthor))+lineEnd);
                }
                fileWriter2.write("UserName"+delimiter+"sisUserId"+delimiter+"resubmissionScore"+delimiter+"resubmissionComment"+delimiter+"resubmissionCommentAuthor"+lineEnd);
                for (List<String> data : comments2) {
                    fileWriter2.write(cleanString(data.get(userName))+delimiter+cleanString(data.get(sisUserId))+delimiter+cleanString(data.get(score))+delimiter+cleanString(data.get(comment))+delimiter+cleanString(data.get(commentAuthor))+lineEnd);
                }
                fileWriter1.close();
                fileWriter2.close();

                System.out.println("Text has been written to the file successfully.");

            } catch (IOException e) {
                e.printStackTrace();
            }
        }




    }

    public static String cleanString(String string) {
        return string.replace(";", "").replace("\n", "").replace("\r", "").replace("\t", "").replace(",", "").strip();
    }

    public static List<List<String>> getQuiz(String canvasUrl, String tokenString, String courseId, String quizTitle) throws IOException {

        OauthToken oauthToken = new NonRefreshableOauthToken(tokenString);
        CanvasApiFactory apiFactory = new CanvasApiFactory(canvasUrl);
        QuizReader quizReader = apiFactory.getReader(QuizReader.class, oauthToken);
        SubmissionReader submissionReader = apiFactory.getReader(SubmissionReader.class, oauthToken);
        List<Quiz> quizzes = quizReader.getQuizzesInCourse(courseId);
        List<List<String>> comments = new ArrayList<>();
        int nateCount = 0;
        int vickiCount = 0;
        for (Quiz quiz : quizzes) {
            if (quiz.getTitle().equals(quizTitle)) {
                GetSubmissionsOptions options = new GetSubmissionsOptions(courseId, quiz.getAssignmentId());
                List<GetSubmissionsOptions.Include> includes = new ArrayList<>();
                includes.add(GetSubmissionsOptions.Include.SUBMISSION_COMMENTS);
                includes.add(GetSubmissionsOptions.Include.USER);
                options.includes(includes);
                List<Submission> submissions = submissionReader.getCourseSubmissions(options);
                for (Submission submission : submissions) {
                    User user = submission.getUser();
                    String userName = user.getName();
                    String sisUserId = user.getSisUserId();
                    double score = submission.getScore();
                    List<SubmissionComment> submissionComments = submission.getSubmissionComments();
                    for (SubmissionComment comment : submissionComments) {
                        System.out.println("*"+comment.getAuthorName());
                        if (!comment.getAuthorName().equals("Nate Stott")) {
                            vickiCount++;
                            System.out.println();
                            System.out.println("************");
                            System.out.println("User Name: ");
                            System.out.println(userName);
                            System.out.println("-");
                            System.out.println("SIS User ID: ");
                            System.out.println(sisUserId);
                            System.out.println("-");
                            System.out.println("Author Name: ");
                            System.out.println(comment.getAuthorName());
                            System.out.println("-");
                            System.out.println("Comment: ");
                            System.out.println(comment.getComment());
                            System.out.println("-");
                            System.out.println("Score: ");
                            System.out.println(score);
                            System.out.println("-");
                            System.out.println();
                            List<String> data = new ArrayList<>();
                            data.add(userName);
                            data.add(sisUserId);
                            data.add(comment.getAuthorName());
                            data.add(comment.getComment());
                            data.add(String.valueOf(score));
                            comments.add(data);

                        }
                        else {
                            nateCount++;
                        }

                    }

                }
            }
        }
        System.out.println(nateCount);
        System.out.println(vickiCount);
        System.out.println();
        System.out.println();
        System.out.println();
        return comments;

    }

}
